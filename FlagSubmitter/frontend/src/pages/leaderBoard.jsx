import React, { useEffect, useState } from "react";
import { Table, Tag, Space } from "antd";
import Navbar from "../components/navbar";
import { leaderboard } from "../scripts/remoteActions";
import { useHistory } from "react-router-dom";

const columns = [
  {
    title: "User name",
    dataIndex: "username",
    align: "center",
    render: (text) => <a>{text}</a>,
  },
  {
    title: "Score",
    className: "score",
    dataIndex: "score",
    align: "center",
  },
  {
    title: "Time(Last Submission)",
    className: "time",
    dataIndex: "time",
    align: "center",
  },
];

const LeaderBoard = (props) => {
  let history = useHistory();
  const [dataLb, setDataLb] = useState([]);
  const reRoute = () => {
    history.push("/login");
  };
  useEffect(() => {
    leaderboard()
      .then((data) => {
        console.log("data", data);
        setDataLb(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  return (
    <>
      <Navbar reRoute={reRoute} />
      <div style={{ padding: 50 }}>
        <Table
          columns={columns}
          dataSource={dataLb}
          bordered
          title={() => <h2>{"Leaderboard"}</h2>}
          footer={() => ""}
        />
      </div>
    </>
  );
};

export default LeaderBoard;
