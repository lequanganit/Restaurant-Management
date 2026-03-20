let render = null;
if (status === 'pending') {
    render = setInterval(() => {
    fetch("/api/cook/rerender")
      .then(res => res.json())
      .then(data => {
        if (data.rerender) {
          fetch("/api/cook/rerender", { method: "POST" });
          location.reload();
        }
      });
  }, 5000);
}
else {
    clearInterval(render);
}

// Xử lý nút bấm tiếp nhận và hoàn thành đơn
function tiepNhanAction(orderId) {
  fetch(`/api/cook/accept/${orderId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        showToast("Cập nhật trạng thái thành công", "Thành công", "success");
        setTimeout(() => {
          location.reload();
        }, 1500);
      } else {
        showToast("Cập nhật trạng thái thất bại", "Lỗi", "danger");
      }
    });
}

function hoanThanhAction(orderId, tableName, userId) {
  fetch(`/api/cook/complete/${orderId}`, { 
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ table_name: tableName, user_id: userId }) 
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        showToast("Cập nhật trạng thái thành công", "Thành công", "success");
        setTimeout(() => {
          location.reload();
        }, 1500);
      } else {
        showToast("Cập nhật trạng thái thất bại", "Lỗi", "danger");
      }
    });
}
