from mass_server import get_production_app
from mass_server.core.models import User, UserLevel, AnalysisSystem

app = get_production_app()

user = User()
user.username = 'admin'
user.set_password('admin')
user.user_level = UserLevel.USER_LEVEL_ADMIN
user.save()

a1 = AnalysisSystem()
a1.identifier_name = 'packerdetection'
a1.verbose_name = 'Packer Detection'
a1.save()

a2 = AnalysisSystem()
a2.identifier_name = 'unzip'
a2.verbose_name = 'Archive Unpacker'
a2.save()

a3 = AnalysisSystem()
a3.identifier_name = 'ssdeep'
a3.verbose_name = 'ssdeep File Similarity Analysis'
a3.save()

a4 = AnalysisSystem()
a4.identifier_name = 'upxunpacker'
a4.verbose_name = 'UPX Unpacker'
a4.save()

