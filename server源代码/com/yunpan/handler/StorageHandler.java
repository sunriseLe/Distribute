package com.yunpan.handler;

import com.yunpan.config.ServerConfig;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.LinkedList;

public class StorageHandler {
    private final Configuration conf;
    private final FileSystem hdfs;
    private final String userRoot;

    /*构造函数*/
    public StorageHandler(int userId) throws IOException {
        this(ServerConfig.HADOOP_SERVER_URI, userId);//调用构造函数StorageHandler(String serverURI, int userId)
    }
    /*构造函数*/
    public StorageHandler(String serverURI, int userId) throws IOException{
        this.conf = new Configuration();//创建配置器
        this.hdfs = FileSystem.get(URI.create(serverURI), conf);//获取FileSystem对象，即创建文件系统
        this.userRoot = "/" + String.valueOf(userId);//设置文件系统根目录
    }

    /*为不完整的绝对路径添加根目录组合成,根目录为/userid*/
    private String getRealPath(String path){
        return path.equals("/")?userRoot:userRoot + path;
    }

    /*获取路径的父路径*/
    private String getParentDirPath(String path){
        return path.substring(0, path.lastIndexOf('/'));
    }

    /*就获取文件名*/
    private String getFileName(String filePath){
        return filePath.substring(filePath.lastIndexOf('/')+1);
    }

    /*获取扩展名*/
    private String getFileExtension(String filePath){

        return filePath.substring(filePath.lastIndexOf('.'));
    }

    /*获取不带扩展名的文件名*/
    private String getFileNameWithoutExtension(String filePath){
        return filePath.substring(filePath.lastIndexOf('/')+1, filePath.lastIndexOf('.'));
    }

    /*实现在hdfs中为新用户创建根目录*/
    public boolean createUserRoot() throws IOException{
        return hdfs.mkdirs(new Path(userRoot));
    }

    /*获取dirPath下的文件列表（包括目录），以ItemMetadata数组返回给主调函数*/
    public ItemMetadata[] list(String dirPath) throws IOException{
        FileStatus status[] = hdfs.listStatus(new Path(getRealPath(dirPath)));//调用hdfs的java api：listStatus(）获取文件列表
        LinkedList<ItemMetadata> itemList = new LinkedList<ItemMetadata>();
        //遍历文件信息
        for(int i=0; i<status.length; i++){
            String path = status[i].getPath().toString();//获取一条文件信息
            itemList.add(new ItemMetadata(path.substring(path.lastIndexOf('/') + 1),//获取文件名
                    status[i].getLen(), status[i].isDir(), status[i].getModificationTime()));//获取文件大小、是否为目录，修改时间
        }
        return itemList.toArray(new ItemMetadata[0]);//将list转化为ItemMetadata数组
    }

    /*本地文件上传到hdfs对应路径，调用调用hdfs的java api：copyFromLocalFile(）*/
    public void createFile(String destFilePath, File file) throws IOException {
        hdfs.copyFromLocalFile(true, true, new Path(file.getAbsolutePath()), new Path(getRealPath(destFilePath)));
    }

    /*调用hdfs的java api：mkdir(），在hdfs文件服务器上创建目录（文件夹），返回true/false表示创建是否成功*/
    public boolean createDir(String dirPath) throws IOException{
        return hdfs.mkdirs(new Path(getRealPath(dirPath)));
    }

    /*将hdfs中的文件下载到本地，调用调用hdfs的java api：copyToLocalFile(）*/
    public File getFile(String filePath) throws IOException{
        File tempFile = new File("/tmp", getFileNameWithoutExtension(filePath) + getFileExtension(filePath));//使用/tmp目录缓存文件
        hdfs.copyToLocalFile(new Path(getRealPath(filePath)), new Path(tempFile.getAbsolutePath()));

        return tempFile;//将tmp目录缓存的文件对象返回给主调函数FileController
    }

    /*重命名hdfs中的文件或目录，调用调用hdfs的java api：rename(）*/
    public boolean rename(String oldPath, String newPath) throws IOException{
        return hdfs.rename(new Path(getRealPath(oldPath)), new Path(getRealPath(newPath)));
    }

    /*删除hdfs中的文件或目录，调用调用hdfs的java api：delete(）*/
    public boolean delete(String path) throws IOException{
        return hdfs.delete(new Path(getRealPath(path)), true);
    }

    /*调用hdfs的java api：exits(）检查路径是否存在*/
    public boolean exists(String path) throws IOException{
        return hdfs.exists(new Path(getRealPath(path)));
    }

    /**
     * 文件信息元数据类
     * 属性：名称(name)，文件大小(length)，是否为目录(isDir),修改时间(modificationTime)
     **/
    public class ItemMetadata {
        private String name;
        private long length;
        private boolean isDir;
        private long modificationTime;

        /*构造函数*/
        public ItemMetadata(String name, long length, boolean isDir, long modificationTime) {
            this.name = name;
            this.length = length;
            this.isDir = isDir;
            this.modificationTime = modificationTime;
        }

        /*getter函数*/
        public String getName() {
            return name;
        }

        public long getLength() {
            return length;
        }

        public boolean isDir() {
            return isDir;
        }

        public long getModificationTime() {
            return modificationTime;
        }

    }
}
