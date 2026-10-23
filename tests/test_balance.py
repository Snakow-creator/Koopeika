"""Balance regressions without a live database, Telegram token or rates API."""
import importlib.util
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch


def dependency(name, **attributes):
    module = ModuleType(name)
    module.__dict__.update(attributes)
    return module


class BalanceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user_req = SimpleNamespace(load=AsyncMock())
        self.transaction_req = SimpleNamespace(load=AsyncMock())
        self.balance_req = SimpleNamespace(change=AsyncMock())
        dependencies = {
            'users': dependency('users', user_req=self.user_req),
            'transactions': dependency('transactions', transaction_req=self.transaction_req),
            'balance': dependency('balance', balance_req=self.balance_req),
            'config': dependency('config', conf=SimpleNamespace(cryptorates={})),
            'tasks.logger': dependency('tasks.logger', log=Mock()),
        }
        path = Path(__file__).resolve().parents[1] / 'src/conversion/converter.py'
        spec = importlib.util.spec_from_file_location('balance_under_test', path)
        module = importlib.util.module_from_spec(spec)
        with patch.dict('sys.modules', dependencies):
            spec.loader.exec_module(module)
        self.converter = module.Convert_Balance

    async def test_first_balance_creates_user_before_loading_transactions(self):
        users = {}

        async def load_user(tg_id):
            users.setdefault(tg_id, {'value': 'USD'})
            return SimpleNamespace(user=users[tg_id])

        async def load_transactions(tg_id):
            self.assertIn(tg_id, users)
            return SimpleNamespace(user=users.get(tg_id), transactions=[])

        self.user_req.load.side_effect = load_user
        self.transaction_req.load.side_effect = load_transactions

        result = await self.converter.con_balance(123, {'USD': 1})

        self.assertEqual(result.balance, '0.00')
        self.assertEqual(result.assets_balance, {})
        self.assertEqual(result.assets_share, {})
        self.balance_req.change.assert_awaited_once_with(123, '0.00')

    async def test_offsetting_transactions_have_zero_balance(self):
        user = {'value': 'USD'}
        self.user_req.load.return_value = SimpleNamespace(user=user)
        self.transaction_req.load.return_value = SimpleNamespace(
            user=user,
            transactions=[
                {'value': 'USD', 'amount': '+10'},
                {'value': 'USD', 'amount': '-10'},
            ],
        )

        result = await self.converter.con_balance(123, {'USD': 1})

        self.assertEqual(result.balance, '0.00')
        self.assertEqual(result.assets_balance, {'USD': 0})
        self.assertEqual(result.assets_share, {'USD': '0.00'})
        self.balance_req.change.assert_awaited_once_with(123, '0.00')

    async def test_nonzero_balance_still_converts_currencies(self):
        user = {'value': 'USD'}
        self.user_req.load.return_value = SimpleNamespace(user=user)
        self.transaction_req.load.return_value = SimpleNamespace(
            user=user,
            transactions=[
                {'value': 'USD', 'amount': '+10'},
                {'value': 'EUR', 'amount': '+5'},
            ],
        )

        result = await self.converter.con_balance(123, {'USD': 1, 'EUR': 2})

        self.assertEqual(result.balance, '20.00')
        self.assertEqual(result.assets_balance, {'USD': 10, 'EUR': 5})
        self.assertEqual(result.assets_share, {'USD': '50.00', 'EUR': '50.00'})
        self.balance_req.change.assert_awaited_once_with(123, '20.00')
