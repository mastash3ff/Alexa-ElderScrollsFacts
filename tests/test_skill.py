"""Tests for Facts for Elder Scrolls Alexa skill."""
from unittest.mock import MagicMock
import pytest
from ask_sdk_model import LaunchRequest, IntentRequest, Intent, Slot

import lambda_function as lf


def make_hi(request, session_attrs=None):
    """Minimal HandlerInput mock."""
    hi = MagicMock()
    hi.request_envelope.request = request
    hi.attributes_manager.session_attributes = {} if session_attrs is None else dict(session_attrs)
    rb = MagicMock()
    for m in ("speak", "ask", "set_card", "set_should_end_session"):
        getattr(rb, m).return_value = rb
    hi.response_builder = rb
    return hi


def make_intent(name, slots=None):
    slot_objs = {k: Slot(name=k, value=str(v)) for k, v in (slots or {}).items()}
    return IntentRequest(intent=Intent(name=name, slots=slot_objs))


class TestLaunchRequest:
    def test_can_handle(self):
        assert lf.LaunchRequestHandler().can_handle(make_hi(LaunchRequest()))

    def test_speaks_elder_scrolls_fact(self):
        hi = make_hi(LaunchRequest())
        lf.LaunchRequestHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert "Did you know" in speech

    def test_ends_session(self):
        hi = make_hi(LaunchRequest())
        lf.LaunchRequestHandler().handle(hi)
        hi.response_builder.set_should_end_session.assert_called_once_with(True)


class TestGetNewFactIntent:
    def test_can_handle(self):
        assert lf.GetNewFactIntentHandler().can_handle(make_hi(make_intent("GetNewFactIntent")))

    def test_cannot_handle_wrong_intent(self):
        assert not lf.GetNewFactIntentHandler().can_handle(make_hi(make_intent("OtherIntent")))

    def test_speaks_fact(self):
        hi = make_hi(make_intent("GetNewFactIntent"))
        lf.GetNewFactIntentHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert "Did you know" in speech

    def test_ends_session(self):
        hi = make_hi(make_intent("GetNewFactIntent"))
        lf.GetNewFactIntentHandler().handle(hi)
        hi.response_builder.set_should_end_session.assert_called_once_with(True)


class TestHelpIntent:
    def test_can_handle(self):
        assert lf.HelpIntentHandler().can_handle(make_hi(make_intent("AMAZON.HelpIntent")))

    def test_keeps_session_open(self):
        hi = make_hi(make_intent("AMAZON.HelpIntent"))
        lf.HelpIntentHandler().handle(hi)
        hi.response_builder.ask.assert_called_once()
        hi.response_builder.set_should_end_session.assert_not_called()


class TestCancelStopIntent:
    @pytest.mark.parametrize("name", ["AMAZON.CancelIntent", "AMAZON.StopIntent"])
    def test_can_handle(self, name):
        assert lf.CancelOrStopIntentHandler().can_handle(make_hi(make_intent(name)))

    def test_says_goodbye(self):
        hi = make_hi(make_intent("AMAZON.StopIntent"))
        lf.CancelOrStopIntentHandler().handle(hi)
        assert "Goodbye" in hi.response_builder.speak.call_args[0][0]

    def test_ends_session(self):
        hi = make_hi(make_intent("AMAZON.CancelIntent"))
        lf.CancelOrStopIntentHandler().handle(hi)
        hi.response_builder.set_should_end_session.assert_called_once_with(True)


class TestFactBank:
    def test_has_facts(self):
        assert len(lf.FACTS) >= 10

    def test_fact_speech_prefix(self):
        speech = lf._get_fact_speech()
        assert speech.startswith("Here's your Elder Scrolls fact: Did you know")

    def test_facts_are_strings(self):
        assert all(isinstance(f, str) for f in lf.FACTS)
