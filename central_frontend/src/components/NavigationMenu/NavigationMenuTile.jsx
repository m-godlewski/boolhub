export default function NavigationMenuTile({ onClick, icon }) {
  return (
    <div className="navigation-menu-tile" onClick={onClick}>
      {icon}
    </div>
  );
}
