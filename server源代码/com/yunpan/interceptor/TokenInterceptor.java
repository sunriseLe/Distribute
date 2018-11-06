package com.yunpan.interceptor;

import com.jfinal.aop.Interceptor;
import com.jfinal.aop.Invocation;
import com.jfinal.core.Controller;
import com.yunpan.controller.FileController;
import com.yunpan.controller.UserController;
import com.yunpan.handler.StorageHandler;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

public class TokenInterceptor implements Interceptor {
    @Override
    public void intercept(Invocation inv) {
        Controller controller = inv.getController();
        HttpServletRequest request = controller.getRequest();
        if((request.getMethod().equals("POST"))&&(request.getContentType().contains("multipart/form-data"))){
            controller.getFile();
        }
        String token = controller.getPara("token");//获取客户端token
        if(token == null){//token为null，表明用户未登录
            controller.setAttr("status", 400);
            controller.setAttr("result", "请登录");
            controller.renderJson();
        }
        else{//token不为null，检查用户身份合法性
            int userId = UserController.tokenValidate(token);
            if(userId == -1){
                controller.setAttr("status", 400);
                controller.setAttr("result", "请登录");
                controller.renderJson();
            }
            else{
                if(controller instanceof FileController){
                    try {
                        ((FileController) controller).setStorage(new StorageHandler(userId));
                        inv.invoke();
                    } catch (IOException e) {
                        controller.setAttr("status", 500);
                        controller.setAttr("result", "服务器内部错误");
                        controller.renderJson();
                    }
                }
            }
        }
    }

}
