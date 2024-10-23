export default function NavigationMenuTile({ title, onClick }) {
  return (
    <div className="navigation-menu-tile" onClick={onClick}>
      {title}
    </div>
  );
}
