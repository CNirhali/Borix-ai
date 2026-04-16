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
            
            const sourceBadge = clone.querySelector('.order-source');
            if (order.source === 'whatsapp') {
                sourceBadge.innerHTML = '🟢 WhatsApp';
                sourceBadge.style.color = '#25D366';
            } else if (order.source === 'telegram') {
                sourceBadge.innerHTML = '✈️ Telegram';
                sourceBadge.style.color = '#38bdf8';
            } else {
                sourceBadge.innerHTML = '🌐 Web';
                sourceBadge.style.color = '#a78bfa';
            }
            
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

            const pushBtn = clone.querySelector('.pos-push-btn');
            if (order.pos_pushed) {
                pushBtn.textContent = 'Pushed to POS';
                pushBtn.disabled = true;
                pushBtn.style.opacity = '0.5';
                pushBtn.style.cursor = 'not-allowed';
            } else {
                pushBtn.addEventListener('click', () => pushOrderToPOS(order.id, pushBtn));
            }

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

    async function pushOrderToPOS(orderId, btnElement) {
        btnElement.textContent = 'Pushing...';
        btnElement.disabled = true;
        try {
            const response = await fetch(`/api/orders/${orderId}/push_pos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pos_name: 'petpooja' })
            });
            const result = await response.json();
            if (result.success) {
                btnElement.textContent = 'Pushed to POS';
                btnElement.style.opacity = '0.5';
                btnElement.style.cursor = 'not-allowed';
                fetchOrders();
            } else {
                btnElement.textContent = 'Push Failed';
                btnElement.style.background = '#ef4444';
                btnElement.disabled = false;
                console.error("Push failed:", result.error);
            }
        } catch (error) {
            console.error("Error pushing to POS:", error);
            btnElement.textContent = 'Push to PetPooja';
            btnElement.disabled = false;
        }
    }

    // Initial fetch
    fetchOrders();
});
