# cleans files

find . -name "*.pyc" -type f -print0 | xargs -0 /bin/rm -f
find . -name ".*" -type f -print0 | xargs -0 /bin/rm -f

git add .
git commit -am "Latest Push"
git push heroku master
