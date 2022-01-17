import React, { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import { Form, Input, Button, Checkbox, Card, notification } from "antd";
import { submit } from "../scripts/remoteActions";
import { useHistory } from "react-router-dom";

const SubmitFlag = (props) => {
  const token = localStorage.getItem("token");

  let history = useHistory();
  if (!token) {
    history.push("/login");
  }
  const reRoute = () => {
    history.push("/login");
  };
  const reRouteSubmit = () => {
    history.push("/submit");
  };
  const onFinish = (values) => {
    console.log("Success:", values);
    const token = localStorage.getItem("token");
    submit(values, token)
      .then((data) => {
        console.log("logged in data", data);
        openNotificationWithIcon("success", "Flag Submitted Successfully");
        localStorage.setItem("token", data.token);
        reRouteSubmit();
      })
      .catch((err) => {
        console.log("err", err.data);
        openNotificationWithIcon("error", "Invalid Entry");
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
          title={"Submit Flag"}
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
              label="Flag"
              name="flag"
              rules={[
                {
                  required: true,
                  message: "Please input your flag!",
                },
              ]}
            >
              <Input />
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

export default SubmitFlag;
