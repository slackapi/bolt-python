from slack_bolt.message_references import (
    CHANNEL_REFERENCE,
    DATE_REFERENCE,
    LINK_REFERENCE,
    SPECIAL_MENTION_REFERENCE,
    UNKNOWN_REFERENCE,
    USER_REFERENCE,
    USERGROUP_REFERENCE,
    SlackMessageReference,
    extract_channel_ids,
    extract_user_ids,
    extract_usergroup_ids,
    parse_slack_references,
)


class TestMessageReferences:
    def test_parse_slack_references(self):
        text = (
            "Hi <@U01V09UNAJZ|some_user>, join <#C123ABC456|general>, "
            "ping <!subteam^SAZ94GDB8|ops>, <!here>, see <https://example.com|docs>, "
            "email <mailto:perihelion@example.com|Email Perihelion>, "
            "and note <!date^1392734382^{date_short}^https://example.com/|Feb 18, 2014 PST>."
        )

        references = parse_slack_references(text)

        assert references == [
            SlackMessageReference(
                type=USER_REFERENCE,
                raw="<@U01V09UNAJZ|some_user>",
                start=text.index("<@U01V09UNAJZ|some_user>"),
                end=text.index("<@U01V09UNAJZ|some_user>") + len("<@U01V09UNAJZ|some_user>"),
                id="U01V09UNAJZ",
                label="some_user",
            ),
            SlackMessageReference(
                type=CHANNEL_REFERENCE,
                raw="<#C123ABC456|general>",
                start=text.index("<#C123ABC456|general>"),
                end=text.index("<#C123ABC456|general>") + len("<#C123ABC456|general>"),
                id="C123ABC456",
                label="general",
            ),
            SlackMessageReference(
                type=USERGROUP_REFERENCE,
                raw="<!subteam^SAZ94GDB8|ops>",
                start=text.index("<!subteam^SAZ94GDB8|ops>"),
                end=text.index("<!subteam^SAZ94GDB8|ops>") + len("<!subteam^SAZ94GDB8|ops>"),
                id="SAZ94GDB8",
                label="ops",
            ),
            SlackMessageReference(
                type=SPECIAL_MENTION_REFERENCE,
                raw="<!here>",
                start=text.index("<!here>"),
                end=text.index("<!here>") + len("<!here>"),
                special_mention="here",
            ),
            SlackMessageReference(
                type=LINK_REFERENCE,
                raw="<https://example.com|docs>",
                start=text.index("<https://example.com|docs>"),
                end=text.index("<https://example.com|docs>") + len("<https://example.com|docs>"),
                url="https://example.com",
                label="docs",
            ),
            SlackMessageReference(
                type=LINK_REFERENCE,
                raw="<mailto:perihelion@example.com|Email Perihelion>",
                start=text.index("<mailto:perihelion@example.com|Email Perihelion>"),
                end=text.index("<mailto:perihelion@example.com|Email Perihelion>")
                + len("<mailto:perihelion@example.com|Email Perihelion>"),
                url="mailto:perihelion@example.com",
                label="Email Perihelion",
            ),
            SlackMessageReference(
                type=DATE_REFERENCE,
                raw="<!date^1392734382^{date_short}^https://example.com/|Feb 18, 2014 PST>",
                start=text.index("<!date^1392734382^{date_short}^https://example.com/|Feb 18, 2014 PST>"),
                end=text.index("<!date^1392734382^{date_short}^https://example.com/|Feb 18, 2014 PST>")
                + len("<!date^1392734382^{date_short}^https://example.com/|Feb 18, 2014 PST>"),
                timestamp="1392734382",
                date_format="{date_short}",
                url="https://example.com/",
                fallback="Feb 18, 2014 PST",
            ),
        ]

        for reference in references:
            assert text[reference.start : reference.end] == reference.raw

    def test_parse_slack_references_without_labels(self):
        text = "<@W123> <#G123> <!subteam^S123> <https://example.com>"

        references = parse_slack_references(text)

        assert references == [
            SlackMessageReference(type=USER_REFERENCE, raw="<@W123>", start=0, end=7, id="W123"),
            SlackMessageReference(type=CHANNEL_REFERENCE, raw="<#G123>", start=8, end=15, id="G123"),
            SlackMessageReference(type=USERGROUP_REFERENCE, raw="<!subteam^S123>", start=16, end=31, id="S123"),
            SlackMessageReference(
                type=LINK_REFERENCE,
                raw="<https://example.com>",
                start=32,
                end=53,
                url="https://example.com",
            ),
        ]

    def test_extract_ids(self):
        text = "<@U111> <@W222|person> <#C111|general> <!subteam^S111|ops> <https://example.com>"

        assert extract_user_ids(text) == ["U111", "W222"]
        assert extract_channel_ids(text) == ["C111"]
        assert extract_usergroup_ids(text) == ["S111"]

    def test_parse_unknown_references(self):
        text = "<@B123|bot> <!unknown|label> <!date^^{date_short}|fallback>"

        references = parse_slack_references(text)

        assert references == [
            SlackMessageReference(type=UNKNOWN_REFERENCE, raw="<@B123|bot>", start=0, end=11, label="bot"),
            SlackMessageReference(type=UNKNOWN_REFERENCE, raw="<!unknown|label>", start=12, end=28, label="label"),
            SlackMessageReference(
                type=UNKNOWN_REFERENCE,
                raw="<!date^^{date_short}|fallback>",
                start=29,
                end=59,
                fallback="fallback",
            ),
        ]

    def test_parse_date_reference_with_caret_in_url(self):
        text = "<!date^1392734382^{date_short}^https://example.com/a^b|Feb 18, 2014 PST>"

        references = parse_slack_references(text)

        assert references == [
            SlackMessageReference(
                type=DATE_REFERENCE,
                raw=text,
                start=0,
                end=len(text),
                timestamp="1392734382",
                date_format="{date_short}",
                url="https://example.com/a^b",
                fallback="Feb 18, 2014 PST",
            )
        ]

    def test_does_not_parse_escaped_or_multiline_angle_brackets(self):
        text = "&lt;@U111&gt; <@U222\n> <@U333>"

        assert parse_slack_references(text) == [
            SlackMessageReference(type=USER_REFERENCE, raw="<@U333>", start=23, end=30, id="U333")
        ]
