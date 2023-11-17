// Використовуємо цей масив, щоб пам'ятати уже відображені order numbers
let displayedOrders = new Set();
let orders_div = document.getElementById("cnt")



// Функція для створення HTML карти замовлення
function createOrderCard(data) {
    // console.log(data)
    var order = document.createElement("div")
    order.setAttribute("class", "order-div")

    var order_header = document.createElement("h5");
    order_header.innerHTML = "id замовлення: " + data[2];
    var name = document.createElement("p");
    name.innerHTML = 'Імя користувача: <b> '+ data[1] +'</b>';
    var strength = document.createElement("li");
    strength.innerHTML = "Міцність: <b>" + data[3] +'</b>';
    var flavor1 = document.createElement("li");
    flavor1.innerHTML = "Основний смак: <b>" + data[4] +"</b>";
    var flavor2 = document.createElement("li");
    flavor2.innerHTML = "Додатковий смак 1: <b>" + data[5] +"</b>";
    var flavor3 = document.createElement("li");
    flavor3.innerHTML = "Додатковий смак 2: <b>" + data[6] +"</b>";

    var list = [order_header, name, strength, flavor1, flavor2, flavor3];

    var container = orders_div.appendChild(order)

    for (item of list){
        container.appendChild(item)
    }

    // console.log(content_container.console)
    ;}

// Функція для отримання замовлень з сервера
function fetchOrders() {
    fetch('api/get_orders') // Тут ваше посилання на API для отримання замовлень
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
setInterval(fetchOrders, 5000);

// Викликаємо функцію відразу при завантаженні сторінки
fetchOrders();