# server:172.25.20.8

## 文件传输

从服务器上下载文件：

`scp username@servername:/path/filename /var/www/local_dir`

上传本地文件到服务器：

`scp /path/filename username@servername:/path `

从服务器下载整个目录

`scp -r username@servername:/var/www/remote_dir/（远程目录） /var/www/local_dir（本地目录）`

上传目录到服务器：



`scp -r local_dir username@servername:remote_dir`