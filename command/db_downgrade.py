import os

os.system("flask --app app.http.app db downgrade")

# base, back to the init version
# os.system("flask --app app.http.app db downgrade base")

# base, back to the 7f3aaa833775 version
# os.system("flask --app app.http.app db downgrade 7f3aaa833775")
