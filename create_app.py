import dtlpy as dl
import os

project_id = os.environ.get('PROJECT_ID')
email = os.environ.get('BOT_EMAIL')
password = os.environ.get('BOT_PASSWORD')
env = os.environ.get('ENV')

dl.setenv(env)
print(f'login with email: {email}')
dl.login_m2m(email=email, password=password)

project = dl.projects.get(project_id=project_id)  # DataloopApps
print(f'publishing to project: {project.name}')

# publish dpk to app store
dpk = dl.dpks.publish()
print(f'published successfully! dpk name: {dpk.name}, dpk id: {dpk.id}')

try:
    app = project.apps.get(app_name=dpk.name)
    print(f'already installed, updating...')
    app.dpk_version = dpk.version
    app.update()
    print(f'update done. app id: {app.id}')
except dl.exceptions.NotFound:
    print(f'installing ..')

    app = project.apps.install(dpk=dpk, app_name=dpk.name)
    print(f'installed! app id: {app.id}')

print(f'Done!')
