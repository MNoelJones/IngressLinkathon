# worldsim_parser.py
from pyparsing import *
from pyparsing import oneOf
from pyparsing import pyparsing_common as ppc
identifier = ppc.identifier
integer = ppc.integer
real = ppc.real
numeric = ppc.numeric

""" BNF:
<portal-id> ::= ID <portalname> '=' <portalguid>

<link-request> ::= LINK <portal> [TO] <portal> [AS <id>]

<field-request> ::= FIELD <portal> <portal> <portal> [AS <id>]

capture-request> ::= CAPTURE <portalname> [AS <id>]

<destroy-link-request> ::= DESTROY <link-id> [AS <id>]
<destroy-portal-request> ::= DESTROY <portalname> [AS <id>]

<deploy-request> ::= DEPLOY <portalname> [<resonator-list>] [AS <id>]

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

<portalguid> ::= <id>

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
        pid = Word(hexnums)
        portalname = (identifier)
        portalguid = Word(hexnums + '.' + hexnums, exact=35)
        as_id = Optional(Suppress(Keyword('AS')) + pid)
        link_id = pid
        portal_id = (
            Suppress(Keyword('ID')) +
            portalname +
            Suppress(Literal('=')) +
            portalguid
        )
        # <lat> ::= ['-'] <intorfloat | <intorfloat>  ['N' | 'S']
        lat = real + Or(Literal('N'), Literal('S'))
        # <lng> ::= ['-'] <intorfloat> | <intorfloat> ['E' | 'W']
        lng = real + Or(Literal('E'), Literal('W'))
        # <latlng> ::= <lat>[,] <lng>
        latlng = lat + Optional(Literal(',')) + lng
        # <portal> ::= <portalname> | <portalguid> | <latlng>
        portal = portalname | portalguid | latlng
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
        destroy_link_request = Forward()
        destroy_link_request <<= (
            pid | destroy_link_request
        )
    # <destroy-portal-ref> ::= <id> | <destroy-portal-request>
        destroy_portal_ref = Forward()
        destroy_portal_ref = (
            pid | destro_portal_ref
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
        command_sequence = (
            Suppress(Keyword("SEQ")) +
            command_entry +
            Optional(command_sequence)
        )
    # <locate-command> ::= LOCATE <portal> [AT] <latlng>
        locate_command = (
            Suppress(Keyword('LOCATE')) +
            portal +
            Ignore(Optional(Keyword('AT'))) +
            latlng
        )
