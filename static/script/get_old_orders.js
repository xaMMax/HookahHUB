// Використовуємо цей масив, щоб пам'ятати уже відображені order numbers
let displayedOrders = new Set();
let orders_div = document.getElementById("cnt");





// Функція для створення HTML карти замовлення
function createOrderCard(data) {
    // console.log(data[0])
    // console.log(data)
    var order = document.createElement("div");
    order.setAttribute("id", "order-div" + data[0])
    order.setAttribute("class", "order-div");


    var order_id = document.createElement("h5");
    order_id.innerHTML = "id замовлення: " + data[1];

    var user_id = document.createElement("p");
    user_id.innerHTML = 'ID користувача: <b> '+ data[2] +'</b>';

    var order_name = document.createElement("li");
    order_name.innerHTML = 'назва замовлення: <b> '+ data[3] +'</b>';

    var strength = document.createElement("li");
    strength.innerHTML = "Міцність: <b>" + data[4] +'</b>';

    var flavor1 = document.createElement("li");
    flavor1.innerHTML = "Основний смак: <b>" + data[5] +"</b>";

    var flavor2 = document.createElement("li");
    flavor2.innerHTML = "Додатковий смак 1: <b>" + data[6] +"</b>";

    var flavor3 = document.createElement("li");
    flavor3.innerHTML = "Додатковий смак 2: <b>" + data[7] +"</b>";

    var confirmed = document.createElement("li");
    if (data[8] = 1){
        confirmed.innerHTML = "Прийнятий до виконання";
    }else{
        confirmed.innerHTML = "Відхилений";
    };

    var deleted_from_admin_page = document.createElement("li");
    if (data[9] = 1){
        deleted_from_admin_page.innerHTML = "Виконаний та видалений з адмін панелі";
    }else{
        deleted_from_admin_page.innerHTML = "Виконаний та видалений з адмін панелі";
    };

    var list = [user_id, order_name, strength, flavor1, flavor2, flavor3, confirmed, deleted_from_admin_page];

    var container = orders_div.appendChild(order)

    for (item of list){
        container.appendChild(item)
    }
    };



// Функція для отримання замовлень з сервера
function fetchOrders() {
   fetch('api/get_old_orders') // Тут ваше посилання на API для отримання замовлень
        .then((response) => response.json())
        .then((orders) => {
            orders.forEach(order => {
                if (!displayedOrders.has(order[0])) {
                    // Якщо замовлення ще не показано, створюємо його картку і додаємо до контейнера
                    const ordersContainer = document.getElementById('cnt');
                    // ordersContainer.insertAdjacentHTML('beforebegin', createOrderCard(order));
                    createOrderCard(order)
                    // Записуємо номер замовлення, як відображений
                    displayedOrders.add(order[0]);
                }
            });
        }).catch(console.error);
}

// Запускаємо функцію fetchOrders кожні 10 секунд
 setInterval(fetchOrders, 10000);

// Викликаємо функцію відразу при завантаженні сторінки
fetchOrders();