import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { PrivateRoute } from "./components/PrivateRoute.jsx";
import Login from "./pages/Login.jsx";
import TasksList from "./pages/TasksList.jsx";
import TaskPage from "./pages/TaskPage.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/tasks" element={
          <PrivateRoute>
            <TasksList />
          </PrivateRoute>
        } />
        
        <Route path="/tasks/new" element={
          <PrivateRoute>
            <TaskPage mode="create" />
          </PrivateRoute>
        } />
        
        <Route path="/tasks/:id" element={
          <PrivateRoute>
            <TaskPage mode="edit" />
          </PrivateRoute>
        } />

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;