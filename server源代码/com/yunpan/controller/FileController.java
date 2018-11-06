package com.yunpan.controller;

import com.jfinal.aop.Before;
import com.jfinal.core.Controller;
import com.jfinal.upload.UploadFile;
import com.yunpan.handler.StorageHandler;
import com.yunpan.interceptor.TokenInterceptor;

import java.io.IOException;

@Before(TokenInterceptor.class)
public class FileController extends Controller {
    private StorageHandler storage;

    public void index() {
        renderText("欢迎来到FileController的世界！");
    }
    /*将新的StorageHandler对象赋值给storage*/
    public void setStorage(StorageHandler storage) {

        this.storage = storage;
    }

    /*创建目录*/
    public void createDir() throws IOException {
        String dirPath = getPara("dirPath");//获取待创建的路径：dirPath
        if(storage.exists(dirPath)){//检查该路径是否存在
            setAttr("status", 403);
            setAttr("result", "路径已存在");//路径已存在，返回result：“路径已存在”
            renderJson();
        }
        else{//路径不存在，则创建该目录
            if(storage.createDir(dirPath)){//成功创建目录
                setAttr("status", 200);
                setAttr("result", "创建成功");
                renderJson();
            }
            else{//创建失败，返回result：“创建失败”
                setAttr("status", 500);
                setAttr("result", "创建失败");
                renderJson();
            }
        }
    }

    /*查看dirptah下的所有文件（包括目录）*/
    public void list() throws IOException{
        String dirPath = getPara("dirPath");
        if(!storage.exists(dirPath)){//路径不存在，返回result：“路径不存在”
            setAttr("status", 403);
            setAttr("result", "路径不存在");
            renderJson();
        }
        else{//路径存在，返回文件或目录列表给客户端（json格式）
            StorageHandler.ItemMetadata[] items = storage.list(dirPath);//调用StorageHandler获取文件（包括目录）列表
            setAttr("status", 200);
            setAttr("result", items);//将获取的文件（包括目录）列表，封装到result中
            renderJson();
        }
    }

    /*将本地文件上传至hdfs*/
    public void upload() {
        UploadFile uploadFile = getFile("file");//上传文件的 File 对象，可以通过 UploadFile.getFile() 直接获取到
        String destDirPath = getPara("destDirPath");//获取待上传文件的目的路径
        String destFilePath = destDirPath + "/" + uploadFile.getOriginalFileName();//将目的路径与文件名合并
        try {
            if (storage.exists(destDirPath)) {//待上传文件的目的路径存在
                if(!storage.exists(destFilePath)){//目的路径下没有待上传的文件
                    storage.createFile(destFilePath, uploadFile.getFile());
                    setAttr("status", 200);
                    setAttr("result", "上传成功");
                }
                else{//目的路径下已有待上传的文件，返回result：“文件已存在”
                    setAttr("status", 403);
                    setAttr("result", "文件已存在");
                }
            } else {//待上传文件的目的路径不存在，返回result：“目录不存在”
                setAttr("status", 403);
                setAttr("result", "目录不存在");
            }
        } catch (IOException e) {
            setAttr("status", 500);
            setAttr("result", "创建失败");
        } finally {
            renderJson();
        }
    }

    /*将hdfs中的文件下载到本地*/
    public void download() throws IOException{
        String filePath = getPara("filePath");
        if(!storage.exists(filePath)){
            setAttr("status", 400);
            setAttr("result", "路径不存在");
            renderJson();
        }
        else{
            renderFile(storage.getFile(filePath));//renderFile用于文件下载
        }
    }

    /*对hdfs中的文件或目录重命名*/
    public void rename() throws IOException{
        String oldPath = getPara("oldPath");
        String newPath = getPara("newPath");
        if(storage.exists(newPath)){//如果新的文件名或目录已存在，返回result：“目标路径已存在”
            setAttr("status", 400);
            setAttr("result", "目标路径已存在");
        }
        else if(storage.rename(oldPath, newPath)){//调用StorageHandler的rename()函数，实现重命名
            setAttr("status", 200);
            setAttr("result", "重命名成功");
        }
        else{
            setAttr("status", 400);
            setAttr("result", "重命名失败，请检查路径");//重命名失败，返回result：“重命名失败，请检查路径”
        }
        renderJson();
    }

    /*对hdfs中的文件或目录进行移动*/
    public void move() throws IOException{
        String oldPath = getPara("oldPath");
        String newPath = getPara("newPath");
        if(storage.rename(oldPath, newPath)){//直接修改路径名，实现移动
            setAttr("status", 200);
            setAttr("result", "移动成功");
        }
        else{
            setAttr("status", 400);
            setAttr("result", "移动失败，请检查路径");
        }
        renderJson();
    }

    /*对hdfs中的文件或目录进行删除*/
    public void delete() throws IOException{
        String path = getPara("path");
        if(storage.delete(path)){//调用StorageHandler的delete()函数，实现删除
            setAttr("status", 200);
            setAttr("result", "删除成功");
        }
        else{
            setAttr("status", 400);
            setAttr("result", "删除失败，请检查路径");//删除失败，返回result：“删除失败，请检查路径”
        }
        renderJson();
    }
}
