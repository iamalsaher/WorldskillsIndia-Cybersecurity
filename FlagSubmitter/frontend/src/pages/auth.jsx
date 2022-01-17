import React, { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import { Form, Input, Button, Checkbox, Card, notification } from "antd";
import { login } from "../scripts/remoteActions";
import { useHistory } from "react-router-dom";

const Auth = (props) => {
  let history = useHistory();
  const token = localStorage.getItem("token");
  if (token) {
    history.push("/submit");
  }
  const reRoute = () => {
    history.push("/login");
  };
  const reRouteSubmit = () => {
    history.push("/submit");
  };
  const onFinish = (values) => {
    console.log("Success:", values);
    login(values)
      .then((data) => {
        console.log("logged in data", data);
        openNotificationWithIcon("success", "Login Successful");
        localStorage.setItem("token", data.token);
        reRouteSubmit();
      })
      .catch((err) => {
        console.log("err", err.data);
        openNotificationWithIcon("error", "Login Failed");
      });
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  const openNotificationWithIcon = (type, message) => {
    notification[type]({
      message: message,
    });
  };
  return (
    <>
      <Navbar reRoute={reRoute} />
      <div style={{ paddingLeft: 50, paddingRight: 50 }}>
        <Card
          bordered={true}
          hoverable={true}
          title={"Login"}
          style={{ borderRadius: 10, zIndex: 1 }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 8,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item
              label="Username"
              name="username"
              rules={[
                {
                  required: true,
                  message: "Please input your username!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Password"
              name="password"
              rules={[
                {
                  required: true,
                  message: "Please input your password!",
                },
              ]}
            >
              <Input.Password />
            </Form.Item>

            <Form.Item
              name="remember"
              valuePropName="checked"
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>
    </>
  );
};

export default Auth;
