import useAuth from "../../hooks/useAuth";

export default function Protected({ children }) {
  const { auth } = useAuth();
  return auth.username ? children : null;

}