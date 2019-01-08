#!/bin/bash

TEST_LIST="tests/vc4_ci/vc4-chamelium.testlist"
RESULT_LOG="result.log"

generate_igtrc() {
cd ~

cat > ".igtrc" <<-EOF
[Common]
FrameDumpPath=/root/
[DUT]
SuspendResumeDelay=15
[Chamelium]
URL=http://${CHAMELIUM_IP}:9992
[Chamelium:${HDMI_DEV_NAME}]
ChameliumPortID=3
EOF

cd - > /dev/null 2>&1
}

usage() {
    echo "usage: $0 -c <chamelium ip address> -h <HDMI device name> -d <igt-gpu-tools dir> [-t <test-list>]" 1>&2
    exit 1
}

while getopts ":c:h:d:t:" opt; do
    case "${opt}" in
        c) CHAMELIUM_IP="${OPTARG}" ;;
        h) HDMI_DEV_NAME="${OPTARG}" ;;
        d) IGT_DIR="${OPTARG}" ;;
        t) TEST_LIST="${OPTARG}" ;;
        *) usage ;;
    esac
done

if [ -z "${CHAMELIUM_IP}" ] || [ -z "${HDMI_DEV_NAME}" ] || [ -z "${IGT_DIR}" ]; then
    usage
fi

# generate ~/.igtrc
if [ ! -f "~/.igtrc" ]; then
    echo "Generate ~/.igtrc"
    generate_igtrc
fi
# Download Piglit
if [ ! -d "${IGT_DIR}/piglit" ]; then
    echo "Download Piglit.."
    ${IGT_DIR}/scripts/run-tests.sh -d
fi
# Run tests
${IGT_DIR}/scripts/run-tests.sh -T ${IGT_DIR}/${TEST_LIST} -v | tee tmp.log
cat tmp.log|grep -e '^pass' -e '^skip' -e '^fail'|awk -F':\ ' '{print $2" "$1}' > ${RESULT_LOG}
