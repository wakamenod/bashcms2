#! /bin/bash -euvx

source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
set -o pipefail

trap 'rm -f $tmp-*' EXIT

### VARIABLES ###
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's:=:s/:')"
md="$contentsdir/$dir/main.md"
[ -f "$md" ]

### MAKE HTML ###
cat << EOF > $tmp-meta.yaml
---
created_time: $(date -f - < $datadir/$dir/created_time)
modified_time: $(date -f - < $datadir/$dir/modified_time)
title: $(grep '^# ' "$md" | sed 's/^# *//')
---
EOF

### OUTPUT ###
#content=$(base64 $md -w 0)
# res=$(curl pandoc-server:8080/v1/convert -X POST \
#     -H 'cache-control: no-cache' \
#     -H 'content-type: application/json' \
#     -d '{
#         "fetcher": {
#             "name": "data",
#             "params": {
#                 "data": "'$content'"
#             }
#         },
#         "converter": {
#             "from": "markdown_github+yaml_metadata_block",
#             "template": "render-html"
#         }
#     }')

# https://stackoverflow.com/questions/3588782/extract-html-tag-data-with-sed
# https://stackoverflow.com/questions/28072190/sed-error-1-not-defined-in-the-re-on-macosx-10-9-5
# https://stackoverflow.com/questions/2777579/how-to-output-only-captured-groups-with-sed
# {"code":0,"message":"","result":{"data":"PGgxPnRpdHRsZTwvaDE+CjxwPldyaXRlIGNvbnRlbnMgaGVyZS48L3A+Cg=="}}
# sed -n -e 's/data":"(.*)"/\1/p'
#            "template": "cms:9786/bashcms2/view/template.html"


# body=$(echo "$res"|sed -n -r 's/^.*"data":"(.*)".*$/\1/p'|base64 -d)

# echo $data
# envsubst < $viewdir/template.html |
# echo $body |

pandoc --template="$viewdir/template.html" \
    -f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml" |
sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;" |
sed "s;/$dir/#;#;g"

    
# temp=$(cat $viewdir/template.html|sed -r 's/\$body\$/'"$data"'/')
