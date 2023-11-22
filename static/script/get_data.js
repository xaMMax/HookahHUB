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
    var buttonsDiv = document.createElement("div");
    buttonsDiv.setAttribute("id", "duttonsDiv");

    var deleteButton = document.createElement("button");
    deleteButton.name = "Delete";
    deleteButton.innerHTML = "Delete";
    deleteButton.setAttribute("id", "delete_btn" + data[0]);
    deleteButton.setAttribute("class", "delete_btn")

    var confirmButton = document.createElement("button");
    confirmButton.name = "Confirm";
    confirmButton.innerHTML = "Confirm";
    confirmButton.setAttribute("id", "confirm_btn" + data[0]);
    confirmButton.setAttribute("class", "confirm_btn")

    // var buttonsDiv = new buttonsDiv;
    var buttonsList = [deleteButton, confirmButton];
    for (item of buttonsList){
        buttonsDiv.appendChild(item)
    };


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

    var list = [order_header, name, strength, flavor1, flavor2, flavor3, buttonsDiv];

    var container = orders_div.appendChild(order)

    for (item of list){
        container.appendChild(item)
    }
    var hideButtonOnclick = document.getElementById("delete_btn" + data[0]);
    hideButtonOnclick.addEventListener("click", function hide(id) {
        const hideBtnId = document.getElementById("delete_btn" + data[0]);
        var buttonIdSlise = id.target.id.slice(-2);
        var oredrIdSlise = order.id.slice(-2);
        console.log(buttonIdSlise, oredrIdSlise);
        order.style.display="none";       
    });
    var confirmButtonOnclick = document.getElementById("confirm_btn" + data[0]);
    confirmButtonOnclick.addEventListener("click", function hide(id) {
        const confirmBtnId = document.getElementById("confirm_btn" + data[0]);
        var buttonIdSlise = id.target.id.slice(-2);
        var oredrIdSlise = order.id.slice(-2);
        console.log(buttonIdSlise, oredrIdSlise);
        order.style.backgroundColor = "rgba(69, 158, 0, 0.60)";       
    });
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

// Запускаємо функцію fetchOrders кожні 5 секунд
setInterval(fetchOrders, 5000);

// Викликаємо функцію відразу при завантаженні сторінки
fetchOrders();