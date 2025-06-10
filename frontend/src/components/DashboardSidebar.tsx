import { Dialog, Disclosure, Transition } from '@headlessui/react';
import { ChevronDownIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { Link, usePage } from '@inertiajs/react';
import { Fragment, useMemo } from 'react';
import { CommonProps } from '@/types/CommonProps';
import { getUserType } from '@/utils/userPermissions';
import { SidebarNavMenuItem } from './SidebarNavMenuItem';
import { PaulLogoSvg } from './PaulLogoSvg';
import classNames from 'classnames';
import { navigation } from '@/constants/staffNavigation';
import { apiGetUrls } from '@/constants/apiUrls';

type DashboardSidebarProps = {
  handleClose: () => void;
  open: boolean;
};

export function DashboardSidebar({ handleClose, open }: DashboardSidebarProps) {
  const {
    url,
    props: { user },
  } = usePage<CommonProps>();

  const userType = user ? getUserType(user) : 'admin_basic';

  const filteredNavigation = useMemo(
    () =>
      navigation
        .filter((navItem) => navItem.userTypes.includes(userType))
        .filter(
          (navItem) =>
            !navItem.href?.includes('audit') || user?.is_admin_member,
        ),
    [user?.is_admin_member, userType],
  );

  const navItems = useMemo(
    () =>
      filteredNavigation.map((item) =>
        !item.href ? (
          <Disclosure key={item.name}>
            <Disclosure.Button className='group flex items-center gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold w-full text-black hover:bg-yellow-400'>
              <item.icon
                className='h-6 w-6 shrink-0 group-hover:text-black'
                aria-hidden='true'
              />
              {item.name}
              <ChevronDownIcon className='h-5 ml-auto' />
            </Disclosure.Button>
            <Disclosure.Panel className='flex flex-col pl-10'>
              {item.items?.map((subItem) => (
                <Link
                  className={classNames(
                    url.split('?')[0].endsWith(subItem.href ?? '')
                      ? 'bg-yellow-400 text-black'
                      : 'text-black hover:bg-yellow-400',
                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold',
                  )}
                  href={subItem.href ?? ''}
                  key={subItem.name}
                >
                  <subItem.icon
                    className={classNames(
                      url.split('?')[0].endsWith(subItem.href ?? '')
                        ? 'text-black'
                        : 'group-hover:text-black',
                      'h-5 w-5 shrink-0',
                    )}
                  />
                  {subItem.name}
                </Link>
              ))}
            </Disclosure.Panel>
          </Disclosure>
        ) : (
          <SidebarNavMenuItem
            active={url.split('?')[0].endsWith(item.href)}
            key={item.name}
            href={item.href}
            {...item}
          />
        ),
      ),
    [filteredNavigation, url],
  );

  const homeUrl = !user
    ? '/'
    : apiGetUrls.dashboard(Boolean(user.is_admin_member));

  return (
    <>
      <Transition.Root show={open} as={Fragment}>
        <Dialog
          as='div'
          className='relative z-50 xl:hidden'
          onClose={handleClose}
        >
          <Transition.Child
            as={Fragment}
            enter='transition-opacity ease-linear duration-300'
            enterFrom='opacity-0'
            enterTo='opacity-100'
            leave='transition-opacity ease-linear duration-300'
            leaveFrom='opacity-100'
            leaveTo='opacity-0'
          >
            <div className='fixed inset-0 bg-gray-900/80' />
          </Transition.Child>

          <div className='fixed inset-0 flex'>
            <Transition.Child
              as={Fragment}
              enter='transition ease-in-out duration-300 transform'
              enterFrom='-translate-x-full'
              enterTo='translate-x-0'
              leave='transition ease-in-out duration-300 transform'
              leaveFrom='translate-x-0'
              leaveTo='-translate-x-full'
            >
              <Dialog.Panel className='relative mr-16 flex w-full max-w-xs flex-1'>
                <Transition.Child
                  as={Fragment}
                  enter='ease-in-out duration-300'
                  enterFrom='opacity-0'
                  enterTo='opacity-100'
                  leave='ease-in-out duration-300'
                  leaveFrom='opacity-100'
                  leaveTo='opacity-0'
                >
                  <div className='absolute left-full top-0 flex w-16 justify-center pt-5'>
                    <button
                      type='button'
                      className='-m-2.5 p-2.5'
                      onClick={handleClose}
                    >
                      <span className='sr-only'>Close sidebar</span>
                      <XMarkIcon
                        className='h-6 w-6 text-white'
                        aria-hidden='true'
                      />
                    </button>
                  </div>
                </Transition.Child>

                {/* Sidebar component, swap this element with another sidebar if you like */}
                <div className='flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4'>
                  <div className='flex h-16 shrink-0 items-center'>
                    <Link href={homeUrl} className='inline-block w-10/12'>
                      <PaulLogoSvg />
                    </Link>
                  </div>
                  <nav className='flex flex-1 flex-col'>
                    <ul className='flex flex-1 flex-col gap-y-7'>
                      <li>
                        <ul className='-mx-2 space-y-1'>{navItems}</ul>
                      </li>
                    </ul>
                  </nav>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition.Root>

      {/* Static sidebar for desktop */}
      <div className='hidden xl:fixed xl:inset-y-0 xl:z-50 xl:flex xl:w-72 xl:flex-col'>
        {/* Sidebar component, swap this element with another sidebar if you like */}
        <div className='flex grow flex-col overflow-y-auto  border-gray-200 bg-white  pb-4'>
          <div className='flex h-16 shrink-0 items-center border-b px-6'>
            <Link href={homeUrl} className='inline-block w-full'>
              <PaulLogoSvg />
            </Link>
          </div>
          <nav className='flex flex-1 flex-col px-6 border-r pt-5'>
            <ul className='-mx-2 space-y-1'>{navItems}</ul>
          </nav>
        </div>
      </div>
    </>
  );
}
