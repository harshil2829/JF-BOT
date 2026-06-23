import Sidebar from "@/components/Sidebar";

export const metadata = {
  title: "JF Bot Admin Panel",
  description: "Admin panel for managing Telegram bots and keys",
};

export default function DashboardLayout({ children }) {
  return (
    <div className="layout-container" style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Sidebar />
      <div className="main-content" style={{ flex: 1, overflowY: 'auto', backgroundColor: '#000', color: '#fff' }}>
        {children}
      </div>
    </div>
  );
}
