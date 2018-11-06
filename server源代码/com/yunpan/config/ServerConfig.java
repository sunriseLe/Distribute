package com.yunpan.config;

import com.jfinal.config.*;
import com.jfinal.plugin.activerecord.ActiveRecordPlugin;
import com.jfinal.plugin.c3p0.C3p0Plugin;
import com.jfinal.plugin.ehcache.EhCachePlugin;
import com.yunpan.controller.FileController;
import com.yunpan.controller.UserController;
import com.yunpan.model.User;

public class ServerConfig extends JFinalConfig {
    public static final String HADOOP_SERVER_URI = "hdfs://localhost:9000";//Hadoop的NameNode地址
    public static final String MYSQL_URI = "jdbc:mysql://172.17.0.1:3306/yun_user";//URL指向要访问的数据库名yun_user
    public static final String MYSQL_USERNAME = "root";//MySQL配置时的用户名
    public static final String MYSQL_PASSWORD = "lxf2017";//MySQL配置时的密码
    public static final String CACHE_NAME = "yun_cache";//服务器端缓存名称


    @Override
    public void configConstant(Constants me) {
        //开启开发模式,在开发模式下，JFinal 会对每次请求输出报告，如输出本次请求的 Controller、Method 以 及请求所携带的参数。
        me.setDevMode(true);
        me.setBaseUploadPath("/tmp");

    }

    @Override
    /**
     *此方法用来配置 JFinal 访问路由，如下代码配置了将”/hello”映射到 HelloController 这个控 制器 ，
     * 通 过 以 下 的 配 置 ， http://localhost:80/hello 将 访 问 HelloController.index() 方法，
     * 而 http://localhost:80/hello/methodName 将访问到 HelloController.methodName()方法。
     **/
    public void configRoute(Routes me) {
        //根目录Url，由对应的Controller控制器来响应访问
        me.add("/user", UserController.class);//访问路径http://localhost:80/user
        me.add("/file", FileController.class);//访问路径http://localhost:80/file

    }

    @Override
    /**
     * 此方法用来配置 JFinal 的 Plugin，
     * 配置了 C3p0 数据库连接池插件与 ActiveRecord数据库访问插件。
     * 通过以下的配置，可以在应用中使用 ActiveRecord 非常方便地操作数据库。
     * */
    public void configPlugin(Plugins me) {
        // 配置C3p0数据库连接池插件
        C3p0Plugin cp = new C3p0Plugin(MYSQL_URI, MYSQL_USERNAME, MYSQL_PASSWORD);
        me.add(cp);
        // 配置ActiveRecord插件
        ActiveRecordPlugin arp =new ActiveRecordPlugin(cp);
        me.add(arp);

        // 映射mysql数据库中的user表到 User模型
        arp.addMapping("user", User.class);
        me.add(new EhCachePlugin());

    }

    @Override
    public void configInterceptor(Interceptors me) {

    }

    @Override
    public void configHandler(Handlers me) {

    }
}
