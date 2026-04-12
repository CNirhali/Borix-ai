document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const ordersGrid = document.getElementById('orders-grid');
    const activeOrdersCount = document.getElementById('active-orders-count');
    const pendingItemsCount = document.getElementById('pending-items-count');
    const template = document.getElementById('order-card-template');

    // Polling interval for dashboard updates
    setInterval(fetchOrders, 2000);

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessageToChat(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.textContent = text;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return msgDiv;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // User message
        addMessageToChat(text, 'user');
        chatInput.value = '';

        // Add typing indicator
        const typingMsg = addMessageToChat("Bot is typing...", 'typing');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            // Remove typing indicator
            typingMsg.remove();

            // Bot response
            addMessageToChat(data.reply, 'bot');
            
            // Instantly fetch orders to update UI immediately
            fetchOrders();

        } catch (error) {
            console.error("Error sending message:", error);
            typingMsg.remove();
            addMessageToChat("Oops, something went wrong connecting to the server.", 'bot');
        }
    }

    async function fetchOrders() {
        try {
            const response = await fetch('/api/orders');
            const data = await response.json();
            renderOrders(data.orders);
        } catch (error) {
            console.error("Error fetching orders:", error);
        }
    }

    function renderOrders(orders) {
        if (!orders || orders.length === 0) {
            ordersGrid.innerHTML = '<div class="empty-state">Waiting for incoming orders...</div>';
            activeOrdersCount.textContent = '0';
            pendingItemsCount.textContent = '0';
            return;
        }

        let pendingOrders = 0;
        let totalItems = 0;

        ordersGrid.innerHTML = '';
        
        orders.forEach(order => {
            const clone = template.content.cloneNode(true);
            const card = clone.querySelector('.order-card');
            
            clone.querySelector('.order-id').textContent = `#${order.id}`;
            clone.querySelector('.order-raw-msg').textContent = `"${order.customer_message}"`;
            
            const statusBadge = clone.querySelector('.order-status');
            statusBadge.textContent = order.status.charAt(0).toUpperCase() + order.status.slice(1);
            
            if (order.status === 'completed') {
                statusBadge.className = 'order-status badge-completed';
                card.classList.add('completed');
            } else {
                pendingOrders++;
            }

            const itemsContainer = clone.querySelector('.order-items');
            order.items.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'order-item';
                itemDiv.innerHTML = `
                    <span><span class="qty-badge">${item.quantity}x</span>${item.name}</span>
                    <span>₹${item.price * item.quantity}</span>
                `;
                itemsContainer.appendChild(itemDiv);
                
                if (order.status !== 'completed') {
                    totalItems += item.quantity;
                }
            });

            const completeBtn = clone.querySelector('.complete-btn');
            completeBtn.addEventListener('click', () => markOrderComplete(order.id));

            ordersGrid.appendChild(clone);
        });

        // Update Stats
        activeOrdersCount.textContent = pendingOrders;
        pendingItemsCount.textContent = totalItems;
    }

    async function markOrderComplete(orderId) {
        try {
            await fetch(`/api/orders/${orderId}/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: 'completed' })
            });
            fetchOrders();
        } catch (error) {
            console.error("Error updating order status:", error);
        }
    }

    // Initial fetch
    fetchOrders();
});
