set -e
git add -A .
git commit -m "$1"
git pull
git push -u origin master