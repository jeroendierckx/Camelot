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

import logging
logger = logging.getLogger('camelot.admin.validator.entity_validator')

from sqlalchemy import orm
from object_validator import ObjectValidator

class EntityValidator(ObjectValidator):
    """A validator class validates an entity before flushing it to the database
    and provides the user with feedback if the entity is not ready to flush
    """

    def validate_object( self, obj ):
        """:return: list of messages explaining invalid data
        empty list if object is valid
        """
        session = orm.object_session( obj )
        if session == None:
            return []
        if obj in session.deleted:
            return []
        return super( EntityValidator, self ).validate_object( obj )
