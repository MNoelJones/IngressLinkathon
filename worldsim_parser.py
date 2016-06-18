# worldsim_parser.py
from pyparsing import *
from pyparsing import oneOf, quotedString
from pyparsing import pyparsing_common as ppc
identifier = ppc.identifier
integer = ppc.integer
real = ppc.real
numeric = ppc.numeric

""" BNF:
<pid> ::= <numeric>
<portal-id> ::= ID <portalname> '=' <pid>

<link-request> ::= LINK <portal> [TO] <portal> [AS <id>]

<field-request> ::= FIELD <portal> <portal> <portal> [AS <id>]

capture-request> ::= CAPTURE <portalname> [AS <id>]

<destroy-link-request> ::= DESTROY <link-id> [AS <id>]
<destroy-portal-request> ::= DESTROY <portalname> [AS <id>]

<deploy-request> ::= DEPLOY <portalname> [<resonator-list>] [AS <id>]
<guid-command> ::= GUID <pid> <portalguid>

<link-ref> ::= <id> | <link-request>
<field-ref> ::= <id> | <field-request>
<capture-ref> ::= <id> | <capture-request>
<destroy-link-ref> ::= <id> | <destroy-link-request>
<destroy-portal-ref> ::= <id> | <destroy-portal-request>
<deploy-ref> ::= <id> | <deploy-request>

<link-sequence> ::= <link-ref> [<link-sequence>]

<portal> ::= <portalname> | <portalguid> | <latlng>

<latlng> ::= <lat>[,] <lng>
<intorfloat> ::= <digit>+ ['.' <digit>+]
<lat> ::= ['-'] <intorfloat | <intorfloat>  ['N' | 'S']
<lng> ::= ['-'] <intorfloat> | <intorfloat> ['E' | 'W']

<portalguid> ::= <hexdigit>+ '.' <hexdigit>+

<id> ::= <hexdigit>+

<command-entry> ::= <field-ref> |
                    <capture-ref> |
                    <destroy-link-ref>
                    <destroy-portal-ref> |
                    <deploy-ref> |
                    <link-sequence>

<command-sequence> ::= SEQ <command-entry> [<command-sequence>]

<locate-command> ::= LOCATE <portal> [AT] <latlng>
"""


class WorldsimParser(ParserElement):
    def __init__(self):
        super(WorldsimParser, self).__init__()
        pid = Word(hexnums)
        portalname = (quotedString)
        portalguid = Word(hexnums + '.' + hexnums, exact=35)
        as_id = Optional(Suppress(Keyword('AS')) + pid)
        link_id = pid
        portal_id = (
            Suppress(Keyword('ID')) +
            portalname +
            Suppress(Literal('=') | Keyword('AS')) +
            pid
        )
        guid_command = (
            Suppress(Keyword('GUID')) +
            pid +
            portalguid
        )
        # <lat> ::= ['-'] <intorfloat | <intorfloat>  ['N' | 'S']
        lat = real + Or(Literal('N'), Literal('S'))
        # <lng> ::= ['-'] <intorfloat> | <intorfloat> ['E' | 'W']
        lng = real + Or(Literal('E'), Literal('W'))
        # <latlng> ::= <lat>[,] <lng>
        latlng = lat + Optional(Literal(',')) + lng
        # <portal> ::= <portalname> | <portalguid> | <latlng>
        portal = portalname | portalguid | latlng | pid
        link_request = (
            Suppress(Keyword('LINK')) +
            portal +
            Optional(Suppress(Literal('TO'))) +
            portal +
            as_id
        )
        field_request = (
            Suppress(Keyword('FIELD')) +
            portal + portal + portal +
            as_id
        )
        capture_request = (
            Suppress(Keyword('CAPTURE')) +
            portalname +
            as_id
        )
        destroy_link_request = (
            Suppress(Keyword('DESTROY')) +
            link_id +
            as_id
        )
        resonator_list = (
            OneOrMore(
                Literal('R') +
                oneOf(['1', '2', '3', '4', '5', '6', '7', '8'])
            )
        )
        deploy_request = (
            Suppress(Keyword('DEPLOY')) +
            portalname +
            resonator_list +
            as_id
        )
        link_ref = pid | link_request
        field_ref = (
            pid | field_request
        )
    # <capture-ref> ::= <id> | <capture-request>
        capture_ref = Forward()
        capture_ref <<= (
            pid | capture_request
        )
    # <destroy-link-ref> ::= <id> | <destroy-link-request>
        destroy_link_ref = Forward()
        destroy_link_ref <<= (
            pid | destroy_link_ref
        )
    # <destroy-portal-ref> ::= <id> | <destroy-portal-request>
        destroy_portal_ref = Forward()
        destroy_portal_ref = (
            pid | destroy_portal_ref
        )
    # <deploy-ref> ::= <id> | <deploy-request>
        deploy_ref = (pid | deploy_request)
    # <link-sequence> ::= <link-ref> [<link-sequence>]
        link_sequence = Forward()
        link_sequence <<= link_ref + Optional(link_sequence)

    # <intorfloat> ::= <digit>+ ['.' <digit>+]
    # <portalguid> ::= <id>
    # <id> ::= <hexdigit>+

    # <command-entry> ::= <field-ref> |
    #                     <capture-ref> |
    #                     <destroy-link-ref>
    #                     <destroy-portal-ref> |
    #                     <deploy-ref> |
    #                     <link-sequence>
        command_entry = (
            field_ref |
            capture_ref |
            destroy_link_ref |
            destroy_portal_ref |
            deploy_ref |
            link_sequence
        )
    # <command-sequence> ::= SEQ <command-entry> [<command-sequence>]
        command_sequence = Forward()
        command_sequence <<= (
            Suppress(Keyword("SEQ")) +
            command_entry +
            Optional(command_sequence)
        )
    # <locate-command> ::= LOCATE <portal> [AT] <latlng>
        locate_command = (
            Suppress(Keyword('LOCATE')) +
            portal +
            Suppress(Optional(Keyword('AT'))) +
            latlng
        )
        # <move-command> ::= MOVE <latlng>
        move_command = Suppress(Keyword('MOVE')) + latlng
        # self.parser = OneOrMore(
        #     command_entry ^
        #     portal_id ^
        #     guid_command
        # )
        self.parser = (
            portal_id ^
            field_ref ^
            link_request ^
            locate_command ^
            guid_command ^
            move_command
        )

    def parseString(self, instring):
        return self.parser.parseString(instring)
