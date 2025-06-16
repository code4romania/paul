import { Link } from '@inertiajs/react';
import classNames from 'classnames';
import { SvgIcon } from '@/types/SvgIcon';

type SidebarNavMenuItemProps = {
  active: boolean;
  href: string;
  icon: SvgIcon;
  name: string;
};

export function SidebarNavMenuItem({
  active,
  href,
  icon: Icon,
  name,
}: SidebarNavMenuItemProps) {
  return (
    <li>
      <Link
        href={href}
        className={classNames(
          active
            ? 'bg-yellow-400 text-black'
            : 'text-black hover:bg-yellow-400',
          'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold',
        )}
      >
        <Icon
          className={classNames(
            active ? 'text-black' : 'group-hover:text-black',
            'h-6 w-6 shrink-0',
          )}
          aria-hidden='true'
        />
        {name}
      </Link>
    </li>
  );
}
