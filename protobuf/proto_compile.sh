SCRIPT_PATH=$( cd "$(dirname "$0")" ; pwd )
SCRIPT_PARENT_PATH=`echo ${SCRIPT_PATH%/*}`
DIST_FILEPATH=$SCRIPT_PATH
PROTO_FILEPATH=$SCRIPT_PATH
PROTO_FILENAME=person.proto

python -m grpc_tools.protoc -I $PROTO_FILEPATH $PROTO_FILENAME --python_out=$DIST_FILEPATH 