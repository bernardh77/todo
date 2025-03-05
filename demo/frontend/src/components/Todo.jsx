import { useState, useEffect } from 'react'
import axios from 'axios'
import { CheckCircleIcon, TrashIcon, PlusIcon, XMarkIcon } from '@heroicons/react/24/outline'

export default function Todo() {
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [notification, setNotification] = useState(null)

  // Get CSRF token from cookie
  const getCookie = (name) => {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';')
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  // Configure axios
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFToken'
  axios.defaults.withCredentials = true
  axios.defaults.baseURL = 'http://localhost:8000'  // Add base URL

  // Fetch todos
  const fetchTodos = async () => {
    try {
      const response = await axios.get('/api/todos/')
      setTodos(response.data)
      setLoading(false)
    } catch (err) {
      setError('Failed to fetch todos')
      setLoading(false)
    }
  }

  // Add todo
  const handleSubmit = async (e) => {
    e.preventDefault() // Prevent form submission
    if (!newTodo.trim()) return

    try {
      const response = await axios.post('/api/todos/', {
        title: newTodo
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      })
      setTodos(prevTodos => [response.data, ...prevTodos])
      setNewTodo('')
      showNotification('Task added successfully!')
    } catch (err) {
      setError('Failed to add todo')
      showNotification('Failed to add task', 'error')
    }
  }

  // Toggle todo completion
  const toggleTodo = async (id) => {
    try {
      const todo = todos.find(t => t.id === id)
      const response = await axios.patch(`/api/todos/${id}/`, {
        completed: !todo.completed
      })
      setTodos(prevTodos => prevTodos.map(t => t.id === id ? response.data : t))
      showNotification(todo.completed ? 'Task marked as incomplete' : 'Task marked as complete')
    } catch (err) {
      setError('Failed to update todo')
      showNotification('Failed to update task', 'error')
    }
  }

  // Delete todo
  const deleteTodo = async (id) => {
    try {
      await axios.delete(`/api/todos/${id}/`)
      setTodos(prevTodos => prevTodos.filter(t => t.id !== id))
      showNotification('Task deleted successfully')
    } catch (err) {
      setError('Failed to delete todo')
      showNotification('Failed to delete task', 'error')
    }
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  useEffect(() => {
    fetchTodos()
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg flex items-center space-x-2 ${
          notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'
        } text-white`}>
          <span>{notification.message}</span>
          <button onClick={() => setNotification(null)}>
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      )}

      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
          <p className="text-gray-600 mt-2">Organize your day, achieve your goals</p>
        </div>

        {/* Add Todo Form */}
        <form 
          onSubmit={handleSubmit} 
          className="mb-8"
          method="POST"
          action="/todo/"
        >
          <div className="flex gap-4 bg-white p-4 rounded-lg shadow-sm">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="What needs to be done?"
              className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center gap-2"
            >
              <PlusIcon className="h-5 w-5" />
              <span>Add Task</span>
            </button>
          </div>
        </form>

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <div className="text-red-500 font-medium">{error}</div>
            <button 
              onClick={fetchTodos}
              className="mt-4 text-blue-600 hover:text-blue-800"
            >
              Try Again
            </button>
          </div>
        ) : (
          /* Todo List */
          <div className="space-y-4">
            {todos.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                <p className="text-gray-500">No tasks yet. Add your first task above!</p>
              </div>
            ) : (
              todos.map(todo => (
                <div
                  key={todo.id}
                  className="group flex items-center justify-between p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
                >
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() => toggleTodo(todo.id)}
                      className={`${
                        todo.completed 
                          ? 'text-green-500 hover:text-green-600' 
                          : 'text-gray-400 hover:text-gray-500'
                      } transition-colors duration-200`}
                    >
                      <CheckCircleIcon className="h-6 w-6" />
                    </button>
                    <span className={`${
                      todo.completed 
                        ? 'line-through text-gray-400' 
                        : 'text-gray-700'
                    } transition-colors duration-200`}>
                      {todo.title}
                    </span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm text-gray-400">
                      {new Date(todo.created_at).toLocaleDateString()}
                    </span>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-600 transition-all duration-200"
                    >
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
} 