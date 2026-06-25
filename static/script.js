async function registerUser() {

    const username =
        document.getElementById("username").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const response = await fetch(
        "/register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    alert(data.message);
}
async function loginUser() {

    const email =
        document.getElementById("login_email").value;

    const password =
        document.getElementById("login_password").value;

    const response = await fetch(
        "/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    if (data.access_token) {

        localStorage.setItem(
            "token",
            data.access_token
        );

        window.location.href = "/dashboard";
    }
    else {
        alert(data.message);
    }
}
async function createTodo() {

    const token =
        localStorage.getItem("token");

    const title =
        document.getElementById("title").value;

    const description =
        document.getElementById("description").value;

    const response = await fetch(
        "/todos",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    loadTodos();
}
async function loadTodos() {

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        "/todos",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const todos = await response.json();

    const todoList =
        document.getElementById("todo-list");

    todoList.innerHTML = "";

    todos.forEach(todo => {

        todoList.innerHTML += `
            <div class="todo-card">
                <h4>${todo.title}</h4>
                <p>${todo.description}</p>
                <button onclick="editTodo(${todo.id})">
    Edit
</button>

<button onclick="deleteTodo(${todo.id})">
    Delete
</button>
            </div>
        `;
    });
}
async function deleteTodo(todoId) {

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        `/todos/${todoId}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    alert(data.message);

    loadTodos();
}
if (
    document.getElementById("todo-list")
) {
    loadTodos();
}
function logoutUser() {

    localStorage.removeItem(
        "token"
    );

    window.location.href =
        "/login-page";
}
if (
    window.location.pathname === "/dashboard"
) {

    const token =
        localStorage.getItem("token");

    if (!token) {

        window.location.href =
            "/login-page";
    }
}
async function editTodo(todoId) {

    const newTitle =
        prompt("Enter new title");

    const newDescription =
        prompt("Enter new description");

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        `/todos/${todoId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                title: newTitle,
                description: newDescription
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    loadTodos();
}