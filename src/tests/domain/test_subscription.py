from datetime import datetime
from uuid import uuid4

import pytest
from dateutil.relativedelta import relativedelta

from src.domain.subscription import Subscription


class TestCreateSubscription:
    """
    Test cases for creating and validating subscriptions.
    """

    def test_create_regular_subscription_with_30_days_duration(self):
        """
        Test creating a regular subscription with a 30-day duration.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)

        assert subscription.id is not None
        assert subscription.start_date is not None
        assert (subscription.end_date - subscription.start_date).days == 30
        assert subscription.is_trial is False
        assert subscription.is_active is True

    def test_create_trial_subscription_with_7_days_trial(self):
        """
        Test creating a trial subscription with a 7-day trial.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_trial(user_id, plan_id)

        assert subscription.id is not None
        assert subscription.start_date is not None
        assert (subscription.end_date - subscription.start_date).days == 7
        assert subscription.is_trial is True
        assert subscription.is_active is True

    def test_end_date_before_today_than_expired_subscription(self):
        """
        Test if a subscription with an end date before today is considered
        an expired subscription.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.now() - relativedelta(days=1)

        assert subscription.is_expired is True

    def test_end_date_after_today_than_not_expired_subscription(self):
        """
        Test if a subscription with an end date after today is not considered
        an expired subscription.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.now() + relativedelta(days=1)

        assert subscription.is_expired is False

    def test_end_date_is_today_than_not_expired_subscription(self):
        """
        Test if a subscription with an end date equal to today is not considered
        an expired subscription.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.now()

        assert subscription.is_expired is False


class TestRenewSubscription:
    """
    Test cases for renewing subscriptions.
    """

    def test_when_is_trial_then_upgrade_to_regular_subscription(self):
        """
        Test renewing a trial subscription to a regular subscription.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_trial(user_id, plan_id)
        assert subscription.is_trial is True
        assert (subscription.end_date - subscription.start_date).days == 7

        subscription.renew()
        assert subscription.is_trial is False
        assert (subscription.end_date - subscription.start_date).days == 30

    def test_when_is_regular_and_not_expired_then_extend_30_days(self):
        """
        Test renewing a regular subscription that is not expired to extend
        its duration by 30 days.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        original_end_date = subscription.end_date
        assert subscription.is_trial is False
        assert (subscription.end_date - subscription.start_date).days == 30

        subscription.renew()
        assert subscription.is_trial is False
        assert (subscription.end_date - original_end_date).days == 30

    def test_when_is_regular_and_expired_then_extend_duration_starting_today(self):
        """
        Test renewing a regular subscription that is expired to extend
        its duration by 30 days starting from today.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.start_date = datetime.now() - relativedelta(days=31)
        subscription.end_date = datetime.now() - relativedelta(days=1)
        original_start_date = subscription.start_date
        original_end_date = subscription.end_date

        assert subscription.is_expired is True

        subscription.renew()
        assert subscription.is_trial is False
        assert subscription.start_date == original_start_date
        assert (subscription.end_date - original_end_date).days == 30

    def test_when_subscription_is_canceled_then_cannot_renew(self):
        """
        Test that a canceled subscription cannot be renewed.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.cancel()
        assert subscription.is_cancelled is True

        with pytest.raises(ValueError, match="Cannot renew a cancelled subscription."):
            subscription.renew()


class TestConvertToTrial:
    """
    Test cases for converting subscriptions to trial.
    """

    def test_when_subscription_is_trial_then_raise_exception(self):
        """
        Test that converting a trial subscription to trial raises an exception.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_trial(user_id, plan_id)
        assert subscription.is_trial is True

        with pytest.raises(ValueError, match="Subscription is already a trial."):
            subscription.convert_to_trial()

    def test_when_subscription_is_regular_then_convert_to_trial_with_7_days_duration(
        self,
    ):
        """
        Test converting a regular subscription to a trial subscription with a 7-day duration.
        """

        user_id = uuid4()
        plan_id = uuid4()

        subscription = Subscription.create_regular(user_id, plan_id)
        assert subscription.is_trial is False

        subscription.convert_to_trial()
        assert subscription.is_trial is True
        assert (subscription.end_date.date() - subscription.start_date.date()).days == 7
