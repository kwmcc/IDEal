# -*- coding: utf-8 -*-
## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('files',
                Field('filename'))

db.files.filename.requires = IS_NOT_EMPTY()
