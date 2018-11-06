package com.yunpan.controller;

import com.jfinal.core.Controller;
import com.jfinal.plugin.ehcache.CacheKit;
import com.yunpan.config.ServerConfig;
import com.yunpan.handler.StorageHandler;
import com.yunpan.model.User;

import java.security.MessageDigest;
import java.util.Date;

public class UserController extends Controller{
    public void index() {
        renderText("欢迎来到UserController的世界！");
    }

    /*从cache中取数据，验证token是否有效*/
    public static int tokenValidate(String token){
        //CacheKit 是缓存操作工具类,get 方法是从 cache 中取数据
        return CacheKit.get(ServerConfig.CACHE_NAME, token) != null?CacheKit.get(ServerConfig.CACHE_NAME, token):-1;
    }
    /*连接数据库实现用户登录，并给用户派发一个token，用于后续操作的身份验证*/
    public void login() throws Exception{
        String username = getPara("username");
        String password = getPara("password");
        if((username == null)||(password == null)){
            setAttr("status", 400);
            setAttr("result", "请输入用户名和密码");
            renderJson();
        }
        else{
            User user = User.dao.findFirst("select * from user where username='" + username + "'");
            if(user.getStr("password").equals(new HashUtils().hashString(password, "MD5"))){
                String token = new HashUtils().hashString(username + new Date().getTime(), "MD5");
                CacheKit.put(ServerConfig.CACHE_NAME, token, user.getInt("id"));//CacheKit 是缓存操作工具类,put 方法是将数据放入 cache

                setAttr("status", 200);
                setAttr("token", token);
                setAttr("result", "登录成功");
                renderJson();
            }
            else{
                setAttr("status", 403);
                setAttr("result", "用户名或密码错误");//登录失败，返回result：“用户名或密码错误”
                renderJson();
            }
        }
    }
    /*连接数据库实现用户登出*/
    public void logout(){
        if(CacheKit.get(ServerConfig.CACHE_NAME, getPara("token")) != null){
            CacheKit.remove(ServerConfig.CACHE_NAME, getPara("token"));
            setAttr("status", 200);
            setAttr("result", "登出成功");
            renderJson();
        }
        else{
            setAttr("status", 400);
            setAttr("result", "您未登录");
            renderJson();
        }
    }
    /*连接数据库实现用户注册，并在hdfs中以用户获得的id给用户创建根目录*/
    public void signup(){
        try {
            String username = getPara("username");
            String password = getPara("password");
            if((username == null)||(password == null)){
                setAttr("status", 400);
                setAttr("result", "请输入用户名和密码");
                renderJson();
            }
            else {
                User user = User.dao.findFirst("select * from user where username='" + username + "'");
                if (user!=null&&user.getStr("username").equals(username)){//用户名已经存在，抛出异常
                    throw new Exception();
                }
                else {//用户名不存在，存储用户信息，并在Hadoop中使用userID创建相应的根目录
                    User user1 = new User();
                    //用户密码使用MD5加密后，存储到数据库中
                    user1.set("username", username).set("password", new HashUtils().hashString(password, "MD5")).save();
                    //先新建StorageHandler对象，该对象调用createUserRoot()函数，在hdfs中为新用户创建根目录
                    new StorageHandler(ServerConfig.HADOOP_SERVER_URI, user1.getInt("id")).createUserRoot();
                    setAttr("status", 200);
                    setAttr("result", "注册成功");
                    renderJson();
                }
            }
        }
        catch(Exception e){//用户名已存在，返回result：“用户名已存在”
            System.out.print(e.getMessage());
            setAttr("status", 403);
            setAttr("result", "用户名已存在");
            renderJson();
        }
    }

    /**
     * hash加密算法类
     **/
    public class HashUtils {
        private HashUtils() {

        }
        /*实现hash加密，用户可以自定义加密算法，返回加密后的字符串*/
        public String hashString(String message, String algorithm)
                throws Exception {
            /**MessageDigest 类为应用程序提供信息摘要算法的功能，如 MD5 或 SHA 算法。
             *信息摘要是安全的单向哈希函数，它接收任意大小的数据，并输出固定长度的哈希值。
             * getInstance()，返回实现指定摘要算法的 MessageDigest 对象。
             **/
            MessageDigest digest = MessageDigest.getInstance(algorithm);
            //digest()通过执行诸如填充之类的最终操作完成哈希计算
            byte[] hashedBytes = digest.digest(message.getBytes("UTF-8"));

            return convertByteArrayToHexString(hashedBytes);

        }

        /*将hash加密后的2进制数组转化成16进制串*/
        private String convertByteArrayToHexString(byte[] arrayBytes) {
            StringBuffer stringBuffer = new StringBuffer();
            for (int i = 0; i < arrayBytes.length; i++) {
                stringBuffer.append(Integer.toString((arrayBytes[i] & 0xff) + 0x100, 16)
                        .substring(1));
            }
            return stringBuffer.toString();
        }
    }
}
