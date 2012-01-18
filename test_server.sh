PASTE_RELOAD=True
export PASTE_RELOAD
err=3
while test "$err" -eq 3 ; do
    python filtercoffee.py test_data
    err="$?"
done
