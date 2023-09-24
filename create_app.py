import subprocess
import argparse
import requests
import shutil
import json
import os
import dtlpy as dl

PANEL_NAME = 'referenceViewer'


def bump(bump_type):
    with os.popen(f'npm version {bump_type} --no-git-tag-version --tag-version-prefix=""') as f:
        version = f.read().strip()
    print(f'Building panel name: {PANEL_NAME}, version: {version}')
    print(f'Bumping version')
    subprocess.check_output(f'git add .', shell=True)
    subprocess.check_output(f'git commit -am "Bump version: v{version}"', shell=True)
    subprocess.check_output('git push', shell=True)
    subprocess.check_output(f'bumpversion --new-version {version} --allow-dirty dummy-part', shell=True)
    subprocess.check_output('git push --follow-tags', shell=True)


def build():
    subprocess.check_call(f'npm i', shell=True)
    subprocess.check_call(f'npm run build', shell=True)

    print(f'Copying dist to panels/{PANEL_NAME}')
    src_dir = os.path.join('dist')
    dst_dir = os.path.join('panels', PANEL_NAME)
    # clean destination
    if os.path.isdir(dst_dir):
        shutil.rmtree(dst_dir)
    # move dist folder
    shutil.move(src=src_dir, dst=dst_dir)
    if not os.path.isdir(dst_dir):
        raise Exception(f'Directory {dst_dir} doesnt exists (and it should be)')


def publish_and_install(project_id):
    success = True
    env = dl.environment()
    with open('dataloop.json') as f:
        manifest = json.load(f)
    app_name = manifest['name']
    app_version = manifest['version']
    user = os.environ.get('GITHUB_ACTOR', dl.info()['user_email'])
    try:
        if project_id is None:
            raise ValueError("Must input project_id to publish and install")
        print(f'Deploying to env : {dl.environment()}')

        project = dl.projects.get(project_id=project_id)  # DataloopApps

        print(f'publishing to project: {project.name}')

        # publish dpk to app store
        dpk = project.dpks.publish()
        print(f'published successfully! dpk name: {dpk.name}, version: {dpk.version}, dpk id: {dpk.id}')

        try:
            app = project.apps.get(app_name=dpk.display_name)
            print(f'already installed, updating...')
            app.dpk_version = dpk.version
            app.update()
            print(f'update done. app id: {app.id}')
        except dl.exceptions.NotFound:
            print(f'installing ..')

            app = project.apps.install(dpk=dpk, app_name=dpk.display_name)
            print(f'installed! app id: {app.id}')

        print(f'Done!')

    except Exception:
        success = False
    finally:

        status_msg = ':heavy_check_mark: Success :rocket:' if success else ':x: Failure :cry:'

        msg = f"""{status_msg}
        *App*: `{app_name}:{app_version}` => *{env}* by {user}
        """
        webhook = os.environ.get('SLACK_WEBHOOK')
        if webhook is None:
            print('WARNING: SLACK_WEBHOOK is None, cannot report')
        else:
            resp = requests.post(url=webhook,
                                 json=
                                 {
                                     "blocks": [
                                         {
                                             "type": "section",
                                             "text": {
                                                 "type": "mrkdwn",
                                                 "text": msg
                                             }
                                         }

                                     ]
                                 })
            print(resp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build, Bump, Publish and Install')
    parser.add_argument('--tag', action='store_true', help='Create a version git tag')
    parser.add_argument('--publish', action='store_true', help='Publish DPK and install app')

    parser.add_argument('--project', help='Project to publish and install to')
    parser.add_argument('--bump-type', default='patch', help='Bump version type: "patch"/"prerelease"/"minor"/"major"')
    args = parser.parse_args()

    if args.tag is True:
        # run build also here to check it works before creating the git tag
        build()
        # bump and push the new tag
        bump(bump_type=args.bump_type)

    if args.publish is True:
        publish_and_install(project_id=args.project)
