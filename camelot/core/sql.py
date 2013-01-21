#  ============================================================================
#
#  Copyright (C) 2007-2012 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

"""
This module complements the sqlalchemy sql module, and contains the `metadata` 
variable, which is a global :class:`sqlalchemy.Metadata` object to which all 
tables of the application can be added.
"""

import logging

from sqlalchemy import event, MetaData
import sqlalchemy.sql.operators

from camelot.core.auto_reload import auto_reload
from camelot.core.conf import settings

LOGGER = logging.getLogger('camelot.core.sql')

#
# Singleton metadata object, to be used together with elixir or in SQLAlchemy
# setups with only a single database
#
metadata = MetaData()
metadata.autoflush = False
metadata.transactional = False

event.listen( auto_reload, 'before_reload', metadata.clear )
    
def like_op(column, string):
    return sqlalchemy.sql.operators.like_op(column, '%%%s%%'%string)

def update_database_from_model():
    """Introspection the model and add missing columns in the database.    
    this function can be ran in setup_model after::
    
        metadata.create_all()
        
    """
    migrate_engine = settings.ENGINE()
    migrate_connection = migrate_engine.connect()
    
    from sqlalchemy.schema import MetaData 
    from migrate.versioning import schemadiff
    from migrate.changeset import create_column
    schema_diff = schemadiff.SchemaDiff(metadata, MetaData(migrate_connection, reflect=True))
   
    for table_name, difference in schema_diff.tables_different.items():
        for column in difference.columns_missing_from_B:
            LOGGER.warn( 'column %s missing in table %s'%(column, table_name) )
            table = metadata.tables[table_name]
            create_column(column, table)
