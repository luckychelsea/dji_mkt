#!/usr/bin/env python
import os
from json import dump

from bitfield import BitField
from django import setup
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import ImageField

from djing.fields import MACAddressField


class BatchSaveStreamList(list):
    def __init__(self, model_class, model_name, except_fields=None, choice_list_map=None, field_name_map=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model_class = model_class
        self._model_name = model_name
        self._except_fields = (except_fields or []) + ['id']
        self._choice_list_map = choice_list_map or {}
        self._field_name_map = field_name_map or {}

    def _map_field_name(self, name):
        if name in self._field_name_map:
            return self._field_name_map.get(name)
        return name

    def _fields(self, obj):
        return {self._map_field_name(ob.name): self._field_val(obj, ob) for ob in obj._meta.concrete_fields if
                ob.name not in self._except_fields}

    def __iter__(self):
        for d in self._model_class.objects.all().iterator():
            yield {
                "model": self._model_name,
                "pk": d.pk,
                "fields": self._fields(d)
            }

    def _field_val(self, obj, field):
        # related fields
        if field.is_relation:
            val = getattr(obj, field.attname)
            return val

        # choice fields
        elif field.name in self._choice_list_map.keys():
            val = getattr(obj, field.name)
            return self._choice_list_map[field.name].get(val)

        # bit fields
        elif isinstance(field, BitField):
            val = getattr(obj, field.name)
            # val is instance of BitHandler
            return int(val)

        # image fields
        elif isinstance(field, ImageField):
            val = getattr(obj, field.name)
            if val._file:
                return val.url

        # mac address validated by netaddr.EUI
        elif isinstance(field, MACAddressField):
            val = getattr(obj, field.name)
            return str(val)

        # all other simple fields
        else:
            v = getattr(obj, field.name)
            if isinstance(v, bool):
                return v
            return v or None

    def __len__(self):
        return 1


def batch_save(fname, *args, **kwargs):
    sa = BatchSaveStreamList(*args, **kwargs)
    with open(fname, 'w') as f:
        dump(sa, f, ensure_ascii=False, indent=2, cls=DjangoJSONEncoder)


# ---------------------


def dump_groups():
    from group_app.models import Group
    batch_save("groups.json", Group, 'groupapp.group')


def dump_accounts():
    from accounts_app.models import UserProfile, BaseAccount, UserProfileLog
    batch_save('accounts_baseaccount.json', BaseAccount, 'profiles.baseaccount')
    batch_save('accounts_userprofile.json', UserProfile, 'profiles.userprofile')
    do_type_map = {
        'cusr': 1,
        'dusr': 2,
        'cdev': 3,
        'ddev': 4,
        'cnas': 5,
        'dnas': 6,
        'csrv': 7,
        'dsrv': 8
    }
    batch_save('accounts_userprofilelog.json', UserProfileLog, 'profiles.userprofilelog',
               except_fields=['meta_info'],
               choice_list_map={
                   'do_type': do_type_map
               })


def dump_messenger():
    from messenger.models import Messenger, ViberMessenger, ViberMessage, ViberSubscriber
    batch_save("messenger.json", Messenger, 'messenger.messenger')
    batch_save("ViberMessenger.json", ViberMessenger, 'messenger.vibermessenger')
    batch_save("ViberMessage.json", ViberMessage, 'messenger.vibermessage')
    batch_save("ViberSubscriber.json", ViberSubscriber, 'messenger.vibersubscriber')


def dump_services():
    from tariff_app.models import Tariff, PeriodicPay
    batch_save("services.json", Tariff, 'services.service', field_name_map={
        'speedIn': 'speed_in',
        'speedOut': 'speed_out',
        'amount': 'cost'
    }, choice_list_map={
        'calc_type': {
            'Df': 0,
            'Dp': 1,
            'Cp': 2,
            'Dl': 3
        }
    })
    batch_save("services_periodicpay.json", PeriodicPay, 'services.periodicpay', choice_list_map={
        'calc_type': {
            'df': 0,
            'cs': 1
        }
    })


def dump_gateways():
    from gw_app.models import NASModel
    batch_save("gateways.json", NASModel, 'gateways.gateway', field_name_map={
        'nas_type': 'gw_type',
        'default': 'is_default'
    }, choice_list_map={
        'nas_type': {
            'mktk': 0
        }
    })


def dump_devices():
    from devapp.models import Device, Port
    batch_save("devices.json", Device, 'devices.device', field_name_map={
        'devtype': 'dev_type'
    }, choice_list_map={
        'devtype': {
            'Dl': 1, 'Pn': 2,
            'On': 3, 'Ex': 4,
            'Zt': 5, 'Zo': 6,
            'Z6': 7, 'Hw': 8
        },
        'status': {
            'und': 0,
            'up': 1,
            'unr': 2,
            'dwn': 3
        }
    })
    batch_save('devices_port.json', Port, 'devices.port')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djing.settings')
    setup()
    dump_devices()
