soxi -D *.wav | awk '{SUM += } END { printf %d:%d:%dn,SUM/3600,SUM%3600/60,SUM%60}'
