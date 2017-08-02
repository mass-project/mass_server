import re
from pymongo import MongoClient
from mongoengine import DoesNotExist
from mass_flask_core.models import SampleRelationType
from mass_flask_core.models import SampleRelation
from mass_flask_config.app import app
import logging
from urllib.parse import urlparse
from collections import namedtuple

logger = logging.getLogger('mass_core')

class MigrationError(RuntimeError):
    pass

MigrationStrategy = namedtuple('MigrationStrategy', ['start', 'goal', 'method'])

def strip_relation_type(sample_relation_cls):
    type_mo = re.search('\.(\w+)', sample_relation_cls)
    if type_mo:
        return type_mo.group(1).replace('SampleRelation', '')
    else:
        return None

def schema_migration_v0_to_v1(db):
    logger.info('Migrating from 0.0 to 1.0')
    directed_relations = {
        'DroppedBy',
        'ResolvedBy',
        'ContactedBy',
        'RetrievedBy',
        }
    undirected_relations = {
        'Ssdeep',
        }


    cnt_new_relations = 0
    for rel in db.sample_relation.find({}):
        if 'relation_type' in rel.keys():
            continue
        rel_type = strip_relation_type(rel['_cls'])
        # check if sample_relation_type exists otherwise create it
        try:
            sample_relation_type = SampleRelationType.objects.get(name=rel_type)
        except DoesNotExist:
            sample_relation_type = SampleRelationType()
            sample_relation_type.name = rel_type
            if rel_type in directed_relations:
                sample_relation_type.directed = True
            elif rel_type in undirected_relations:
                sample_relation_type.directed = False
            else:
                raise MigrationError('I hope you have a backup')
            sample_relation_type.description = 'Auto-generated during migration.'
            sample_relation_type.save()

        # create new sample relation with resp type
        new_sample_relation = SampleRelation()
        new_sample_relation.relation_type = sample_relation_type
        new_sample_relation.sample = rel['sample']
        new_sample_relation.other = rel['other']

        # Shitty special case
        if sample_relation_type.name == 'Ssdeep':
            match_value = int(rel['match'])
            new_sample_relation.additional_metadata({'match': match_value})
        new_sample_relation.save()
        cnt_new_relations += 1

    db.sample_relation.delete_many({'relation_type': {'$exists': False}})
    db.create_collection('meta_data')
    logger.info('Setting meta_data')
    db['meta_data'].insert_one({'schema_version': '1.0'})


def schema_migration():
    migration_strategies = [
        MigrationStrategy('0.0', '1.0', schema_migration_v0_to_v1),
        ]

    mongo_client = MongoClient(app.config['MONGODB_SETTINGS']['host'])
    url = urlparse(app.config['MONGODB_SETTINGS']['host'])
    db = mongo_client[url.path[1:]]

    current_schema_version = '0.0'
    ret = db['meta_data'].find_one({'schema_version': {'$exists': True}})
    if ret:
        current_schema_version = ret['schema_version']

    logger.info('Current schema version: {}'.format(current_schema_version))

    while current_schema_version != app.schema_version:
        migration_strategy = [s for s in migration_strategies if s.start == current_schema_version][0]
        logger.info('Migrating from schema {} to schema {}'.format(migration_strategy.start, migration_strategy.goal))
        migration_strategy.method(db)
        current_schema_version = migration_strategy.goal
