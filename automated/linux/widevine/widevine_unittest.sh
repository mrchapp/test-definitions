#!/bin/sh
set -x

CMD="/usr/bin/widevine_ce_cdm_unittest"
LOG_FILE="log.txt"
RESULT_FILE="result.txt"

${CMD} > ${LOG_FILE} 2>&1

# Fix can not loding shared libraries error
if `grep -q "loading shared libraries" ${LOG_FILE}` ; then
    lib=`cat ${LOG_FILE} | awk -F: '{print $3}'`
    dest_dir=`dirname ${lib}`
    lib_name=`basename ${lib}`
    mkdir -p ${dest_dir}
    ln -s /usr/lib/${lib_name} ${dest_dir}
fi

${CMD} | tee ${LOG_FILE} 2>&1

grep "ms)$" ${LOG_FILE} | \
  sed -e 's/\ (.*)$//' \
      -e 's/[[:space:]]*//g' \
      -e 's/=//' \
      -e 's/\[OK\]/pass:/' \
      -e 's/\[FAILED\]/fail:/' | \
  awk -F: '{print $2" "$1}' \
  > ${RESULT_FILE}
