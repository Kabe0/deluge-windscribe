EXIST=`ip route show 128.0.0.0/1 | wc -l`
if [ $EXIST -eq 1 ]
then
    echo "Found offending route, deleting now."
    ip route del 128.0.0.0/1
fi