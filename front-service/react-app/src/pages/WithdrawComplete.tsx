import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  Divider,
  Collapse,
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8002";

const WithdrawComplete: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(location.state?.withdraw || null);
  const [loading, setLoading] = useState(!location.state?.withdraw);
  const [error, setError] = useState("");
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    if (data) return; // 이미 state로 받은 경우 API 호출 안 함
    const access = localStorage.getItem("access_token");
    if (!access) {
      navigate("/login");
      return;
    }
    fetch(`${API_BASE_URL}/api/cash/withdraw/complete/`, {
      headers: { Authorization: `Bearer ${access}` },
    })
      .then(async (res) => {
        if (res.status === 401) {
          navigate("/login");
          throw new Error("인증 실패");
        }
        if (!res.ok) throw new Error("서버 오류");
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [navigate, data]);

  if (loading)
    return (
      <Container sx={{ mt: 8 }}>
        <Typography>로딩 중...</Typography>
      </Container>
    );
  if (error)
    return (
      <Container sx={{ mt: 8 }}>
        <Typography color="error">{error}</Typography>
      </Container>
    );
  if (!data) return null;

  const {
    name,
    email,
    balance,
    previous_balance,
    recent_withdraws = [],
  } = data;

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Button
        onClick={() => navigate("/withdraw")}
        sx={{ mb: 2, color: "#7c4a03" }}
      >
        ← 출금 페이지로 돌아가기
      </Button>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 5, mb: 4 }}>
        <Typography variant="h5" color="#7c4a03" fontWeight={700} gutterBottom>
          <span style={{ fontSize: 32, marginRight: 8 }}>💰</span>출금 상세 정보
        </Typography>
        <Box
          sx={{
            bgcolor: "linear-gradient(90deg, #ffe066 0%, #ffb347 100%)",
            borderRadius: 3,
            p: 3,
            mb: 3,
          }}
        >
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            mb={2}
          >
            <Typography fontWeight={700} fontSize={20}>
              Cash 🏦
            </Typography>
            <Typography fontSize={28}>{email}</Typography>
          </Box>
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
          >
            <Typography fontSize={18}>{name}</Typography>
            <Typography fontWeight={700} fontSize={28} color="#7c4a03">
              ₩ {Number(balance).toLocaleString()}
            </Typography>
          </Box>
        </Box>
        <Divider sx={{ my: 2 }} />
        <Typography variant="h6" color="#7c4a03" gutterBottom>
          출금 내역
        </Typography>
        <Paper sx={{ p: 2, mb: 2, bgcolor: "#fffde7" }}>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <span>출금 금액</span>
            <span className="text-2xl font-bold text-chick-brown">
              ₩ {recent_withdraws[0]?.amount?.toLocaleString() ?? 0}
            </span>
          </Box>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <span>출금 일시</span>
            <span>{recent_withdraws[0]?.created_at ?? "내역 없음"}</span>
          </Box>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <span>거래 ID</span>
            <span>DP2025040154321</span>
          </Box>
          <Box display="flex" justifyContent="space-between">
            <span>상태</span>
            <span
              style={{
                background: "#e0ffe0",
                color: "#388e3c",
                borderRadius: 8,
                padding: "2px 12px",
              }}
            >
              완료
            </span>
          </Box>
        </Paper>
        <Divider sx={{ my: 2 }} />
        <Typography variant="h6" color="#7c4a03" gutterBottom>
          출금 후 잔액
        </Typography>
        <Box display="flex" justifyContent="space-between" mb={1}>
          <span>이전 잔액</span>
          <span>₩ {Number(previous_balance).toLocaleString()}</span>
        </Box>
        <Box display="flex" justifyContent="space-between" mb={1}>
          <span>출금 금액</span>
          <span style={{ color: "#d32f2f" }}>
            - ₩ {recent_withdraws[0]?.amount?.toLocaleString() ?? 0}
          </span>
        </Box>
        <Box
          display="flex"
          justifyContent="space-between"
          fontWeight={700}
          fontSize={18}
        >
          <span>현재 잔액</span>
          <span style={{ color: "#7c4a03" }}>
            ₩ {Number(balance).toLocaleString()}
          </span>
        </Box>
      </Paper>
      {/* 최근 출금 내역 */}
      <Paper elevation={2} sx={{ p: 4, borderRadius: 5 }}>
        <Typography variant="h6" color="#7c4a03" gutterBottom>
          최근 출금 내역
        </Typography>
        {recent_withdraws.length === 0 && (
          <Typography color="text.secondary">출금 내역이 없습니다.</Typography>
        )}
        {(showAll ? recent_withdraws : recent_withdraws.slice(0, 3)).map(
          (tx: any, idx: number) => (
            <Box
              key={tx.id}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              py={1}
              borderBottom={idx < recent_withdraws.length - 1 ? 1 : 0}
              borderColor="#eee"
            >
              <Box>
                <Typography fontWeight={600}>
                  {tx.bank_name || "출금"}
                </Typography>
                <Typography fontSize={14} color="text.secondary">
                  {tx.created_at}
                </Typography>
              </Box>
              <Box textAlign="right">
                <Typography fontWeight={700} color="red">
                  - ₩ {Number(tx.amount).toLocaleString()}
                </Typography>
                <Typography fontSize={14} color="text.secondary">
                  {tx.transaction_method || "계좌 이체"}
                </Typography>
              </Box>
            </Box>
          )
        )}
        {recent_withdraws.length > 3 && (
          <Box textAlign="center" mt={2}>
            <Button
              onClick={() => setShowAll((v) => !v)}
              sx={{ color: "#7c4a03" }}
            >
              {showAll ? "출금 내역 접기" : "모든 출금 내역 보기"}
            </Button>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default WithdrawComplete;
