#!/bin/sh

# test launch commands.
echo TEST

# environment
echo APP_ENV=$APP_ENV
echo APP_NAME=$APP_NAME

# build
echo DISTRIB_ID=$DISTRIB_ID
echo WORKSPACE_FOLDER=$WORKSPACE_FOLDER

# Physical
echo PROJECT_FOLDER=$PROJECT_FOLDER
echo DATA_FOLDER=$DATA_FOLDER

# DEPLOY
echo RESOURCE_CPUS=$RESOURCE_CPUS
echo RESOURCE_GPUS=$RESOURCE_GPUS
echo RESOURCE_MEMORY=$RESOURCE_MEMORY
echo SCALE=$SCALE

# SERVER
echo HOST_IP=$HOST_IP
echo HOST_IP=$HOST_IP
echo HTTP_PORT=$HTTP_PORT
echo HTTPS_PORT=$HTTPS_PORT
echo TCP_PORT=$TCP_PORT
echo SOCKET_PORT=$SOCKET_PORT
echo HTTP_PORT_RANGE=$HTTP_PORT_RANGE
echo HTTPS_PORT_RANGE=$HTTPS_PORT_RANGE
echo TCP_PORT_RANGE=$TCP_PORT_RANGE
echo SOCKET_PORT_RANGE=$SOCKET_PORT_RANGE

# SWICHS
echo SWICH_TRACKING_TRACE=$SWICH_TRACKING_TRACE
echo SWICH_TRACKING_DEBUG=$SWICH_TRACKING_DEBUG
echo SWICH_TRACKING_INFO=$SWICH_TRACKING_INFO
echo SWICH_TRACKING_WARN=$SWICH_TRACKING_WARN
echo SWICH_TRACKING_ERROR=$SWICH_TRACKING_ERROR
echo SWICH_TRACKING_VERBOSE=$SWICH_TRACKING_VERBOSE
echo SWICH_TRACKING_REPORT=$SWICH_TRACKING_REPORT

# Application

echo PYTHONPATH=$PYTHONPATH

echo ==========

. $DATA_FOLDER/.venv/bin/activate
if [ $? -ne 0 ]; then
  echo "✖️ Failed to activate virtual environment."
  exit 1
else
  echo "✅ Virtual environment activated."
fi

black .
if [ $? -ne 0 ]; then
  echo "✖️ Automatically formatting Python code failed."
  exit 1
else
  echo "✅ Automatically formatting Python code succeeded."
fi

flake8
if [ $? -ne 0 ]; then
  echo "✖️ Linting errors found. Please fix them before committing."
  exit 1
else
  echo "✅ Linting passed."
fi

sphinx-apidoc -o /workspaces/template/dist/docs  /workspaces/template/src
if [ $? -ne 0 ]; then
  echo "✖️ Documentation generation code failed."
  exit 1
else
  echo "✅ Automatically the Documentation code was successful."
fi

behave
if [ $? -ne 0 ]; then
  echo "✖️ Behavior-driven development failed."
  exit 1
else
  echo "✅ Behavior-driven development was successful."
fi

# This command tells
# Gunicorn to use the gevent worker class (-k gevent),
# bind the server to the specified host and port (-b $HOST_IP:$HTTP_PORT),
# and run 4 worker processes (-w 4).
# Adjust the number of workers based on your server's resources.

# This command starts Gunicorn and runs the HTTP server on $HOST_IP:$HTTP_PORT
$DATA_FOLDER/.venv/bin/gunicorn -c gunicorn_config.py src.web.app:app
if [ $? -ne 0 ]; then
  echo "✖️ HTTP failed."
  exit 1
else
  echo "✅ HTTP was successful."
fi

# This command will start the WebSocket server.  $HOST_IP:$SOCKET_PORT
# Gunicorn will only process HTTP requests.
# This way both servers will run on different ports.
# $DATA_FOLDER/.venv/bin/python src/web/app.py
# if [ $? -ne 0 ]; then
#   echo "✖️ SOCKET failed."
#   exit 1
# else
#   echo "✅ SOCKET was successful."
# fi

echo ==========

sleep infinity

/bin/sh
