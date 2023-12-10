target-cpu optimization
If you are building for your current CPU platform (for example, build and run on your personal computer), it is recommended to set target-cpu=native feature to let rustc generate and optimize code for the CPU running the compiler.

export RUSTFLAGS="-C target-cpu=native"

ssservice genkey -m "aes-128-gcm"

{
"server": "my_server_ip",
"server_port": 8388,
"password": "rwQc8qPXVsRpGx3uW+Y3Lj4Y42yF9Bs0xg1pmx8/+bo=",
"method": "aes-256-gcm",
// ONLY FOR `sslocal`
// Delete these lines if you are running `ssserver` or `ssmanager`
"local_address": "127.0.0.1",
"local_port": 1080
}

git clone https://git.zx2c4.com/wintun

sslocal -c config.json
ssserver -c config.json

# Read local client configuration from file

sslocal -c /conf/shadowsocks.json
