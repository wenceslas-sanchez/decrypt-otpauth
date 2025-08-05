import pytest
import plistlib


def string_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'NS.string': 'Hello, World!',
                '$class': plistlib.UID(2)
            },
            {
                '$classes': ['NSString', 'NSObject'],
                '$classname': 'NSString'
            }
        ]
    }


def number_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'integers': plistlib.UID(2),
                'floats': plistlib.UID(5),
                'booleans': plistlib.UID(8),
                '$class': plistlib.UID(11)
            },
            {
                'NS.objects': [plistlib.UID(3), plistlib.UID(4)],
                '$class': plistlib.UID(12)
            },
            {'NS.intval': 42, '$class': plistlib.UID(13)},
            {'NS.intval': -123, '$class': plistlib.UID(13)},
            {
                'NS.objects': [plistlib.UID(6), plistlib.UID(7)],
                '$class': plistlib.UID(12)
            },
            {'NS.dblval': 3.14159, '$class': plistlib.UID(13)},
            {'NS.dblval': -2.71828, '$class': plistlib.UID(13)},
            {
                'NS.objects': [plistlib.UID(9), plistlib.UID(10)],
                '$class': plistlib.UID(12)
            },
            {'NS.boolval': True, '$class': plistlib.UID(13)},
            {'NS.boolval': False, '$class': plistlib.UID(13)},
            {'$classes': ['NSDictionary', 'NSObject'], '$classname': 'NSDictionary'},
            {'$classes': ['NSArray', 'NSObject'], '$classname': 'NSArray'},
            {'$classes': ['NSNumber', 'NSValue', 'NSObject'], '$classname': 'NSNumber'}
        ]
    }


def dictionary_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'NS.keys': [plistlib.UID(2), plistlib.UID(3), plistlib.UID(4)],
                'NS.objects': [plistlib.UID(5), plistlib.UID(6), plistlib.UID(7)],
                '$class': plistlib.UID(8)
            },
            {'NS.string': 'name', '$class': plistlib.UID(9)},
            {'NS.string': 'age', '$class': plistlib.UID(9)},
            {'NS.string': 'active', '$class': plistlib.UID(9)},
            {'NS.string': 'John Doe', '$class': plistlib.UID(9)},
            {'NS.intval': 30, '$class': plistlib.UID(10)},
            {'NS.boolval': True, '$class': plistlib.UID(10)},
            {'$classes': ['NSDictionary', 'NSObject'], '$classname': 'NSDictionary'},
            {'$classes': ['NSString', 'NSObject'], '$classname': 'NSString'},
            {'$classes': ['NSNumber', 'NSValue', 'NSObject'], '$classname': 'NSNumber'}
        ]
    }


def array_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'NS.objects': [
                    plistlib.UID(2),
                    plistlib.UID(3),
                    plistlib.UID(4),
                    plistlib.UID(5)
                ],
                '$class': plistlib.UID(9)
            },
            {'NS.string': 'Array Element 1', '$class': plistlib.UID(10)},
            {'NS.intval': 999, '$class': plistlib.UID(11)},
            {'NS.data': b'Hello Binary World!', '$class': plistlib.UID(12)},
            {
                'NS.keys': [plistlib.UID(6)],
                'NS.objects': [plistlib.UID(7)],
                '$class': plistlib.UID(8)
            },
            {'NS.string': 'nested_key', '$class': plistlib.UID(10)},
            {'NS.string': 'nested_value', '$class': plistlib.UID(10)},
            {'$classes': ['NSDictionary', 'NSObject'], '$classname': 'NSDictionary'},
            {'$classes': ['NSArray', 'NSObject'], '$classname': 'NSArray'},
            {'$classes': ['NSString', 'NSObject'], '$classname': 'NSString'},
            {'$classes': ['NSNumber', 'NSValue', 'NSObject'], '$classname': 'NSNumber'},
            {'$classes': ['NSData', 'NSObject'], '$classname': 'NSData'}
        ]
    }

def date_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'creation_date': plistlib.UID(2),
                'timestamp_now': plistlib.UID(3),
                '$class': plistlib.UID(4)
            },
            {'NS.time': 0.0, '$class': plistlib.UID(5)},  # 2001-01-01 00:00:00 UTC
            {'NS.time': 725846400.0, '$class': plistlib.UID(5)},  # ~2024-01-01
            {'$classes': ['NSDictionary', 'NSObject'], '$classname': 'NSDictionary'},
            {'$classes': ['NSDate', 'NSObject'], '$classname': 'NSDate'}
        ]
    }


def complexe_plist():
    return {
        '$version': 100000,
        '$archiver': 'NSKeyedArchiver',
        '$top': {
            'root': plistlib.UID(1)
        },
        '$objects': [
            '$null',
            {
                'accounts': plistlib.UID(2),
                'version': plistlib.UID(9),
                '$class': plistlib.UID(10)
            },
            {
                'NS.objects': [plistlib.UID(3), plistlib.UID(6)],
                '$class': plistlib.UID(11)
            },
            {
                'NS.keys': [plistlib.UID(4), plistlib.UID(5)],
                'NS.objects': [plistlib.UID(12), plistlib.UID(13)],
                '$class': plistlib.UID(10)
            },
            {'NS.string': 'name', '$class': plistlib.UID(14)},
            {'NS.string': 'secret', '$class': plistlib.UID(14)},
            {
                'NS.keys': [plistlib.UID(4), plistlib.UID(5)],
                'NS.objects': [plistlib.UID(7), plistlib.UID(8)],
                '$class': plistlib.UID(10)
            },
            {'NS.string': 'Google', '$class': plistlib.UID(14)},
            {'NS.data': b'JBSWY3DPEHPK3PXP', '$class': plistlib.UID(15)},
            {'NS.dblval': 1.1, '$class': plistlib.UID(16)},
            {'$classes': ['NSDictionary', 'NSObject'], '$classname': 'NSDictionary'},
            {'$classes': ['NSArray', 'NSObject'], '$classname': 'NSArray'},
            {'NS.string': 'GitHub', '$class': plistlib.UID(14)},
            {'NS.data': b'MFRGG2LTEB3GS5LQMFXHC5DSMR2W45A', '$class': plistlib.UID(15)},
            {'$classes': ['NSString', 'NSObject'], '$classname': 'NSString'},
            {'$classes': ['NSData', 'NSObject'], '$classname': 'NSData'},
            {'$classes': ['NSNumber', 'NSValue', 'NSObject'], '$classname': 'NSNumber'}
        ]
    }
