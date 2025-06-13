import { Menu, Transition } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import { Bars3Icon } from '@heroicons/react/24/outline';
import { Link, useForm, usePage } from '@inertiajs/react';
import classNames from 'classnames';
import { Fragment, useCallback } from 'react';
import { apiGetUrls, apiPostUrls } from '@/constants/apiUrls';
import { CommonProps } from '@/types/CommonProps';
import { Avatar } from './Avatar';
import { PaulLogoSvg } from './PaulLogoSvg';

type DashboardTopBarProps = {
  handleOpenSidebar: () => void;
};

export function DashboardTopBar({ handleOpenSidebar }: DashboardTopBarProps) {
  const {
    props: { is_authenticated, user },
  } = usePage<CommonProps>();

  const { post } = useForm();

  const handleSignOut = useCallback(() => {
    post(
      apiPostUrls.usersLogout(user?.is_staff_member ? 'staff' : 'applicants'),
    );
  }, [post, user?.is_staff_member]);

  return (
    <div className='fixed top-0 z-40 left-0 right-0'>
      <div className='flex justify-between h-16 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-md sm:gap-x-6 sm:px-6 xl:shadow-none'>
        <div className='flex gap-6 w-full'>
          {is_authenticated && (
            <button
              type='button'
              className='xl:hidden'
              onClick={handleOpenSidebar}
            >
              <span className='sr-only'>Open sidebar</span>
              <Bars3Icon className='h-6 w-6' aria-hidden='true' />
            </button>
          )}

          <Link
            className='flex w-56'
            href={
              !user ? '/' : apiGetUrls.dashboard(Boolean(user.is_admin_member))
            }
          >
            <PaulLogoSvg />
          </Link>
        </div>

        {is_authenticated && user && (
          <div className='flex gap-x-4 self-stretch xl:gap-x-6'>
            <div className='flex items-center gap-x-4 xl:gap-x-6'>
              {/* Profile dropdown */}
              <Menu as='div' className='relative'>
                <Menu.Button className='-m-1.5 flex items-center p-1.5'>
                  <span className='sr-only'>Open user menu</span>
                  <Avatar size='small' src={user?.avatar} />
                  <span className='hidden xl:flex xl:items-center'>
                    <span
                      className='ml-4 text-sm font-semibold leading-6 text-gray-900'
                      aria-hidden='true'
                    >
                      {user?.first_name} {user?.last_name}
                    </span>
                    <ChevronDownIcon
                      className='ml-2 h-5 w-5 text-gray-400'
                      aria-hidden='true'
                    />
                  </span>
                </Menu.Button>
                <Transition
                  as={Fragment}
                  enter='transition ease-out duration-100'
                  enterFrom='transform opacity-0 scale-95'
                  enterTo='transform opacity-100 scale-100'
                  leave='transition ease-in duration-75'
                  leaveFrom='transform opacity-100 scale-100'
                  leaveTo='transform opacity-0 scale-95'
                >
                  <Menu.Items className='absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-hidden'>
                    <Menu.Item
                      as={Link}
                      className={({ active }) =>
                        classNames(
                          active ? 'bg-gray-50' : '',
                          'block px-3 py-1 text-sm leading-6 text-gray-900',
                        )
                      }
                      href={
                        user.is_applicant_member
                          ? '/applicants/settings/'
                          : apiGetUrls.usersSettings
                      }
                    >
                      Setări
                    </Menu.Item>
                    <Menu.Item
                      as='button'
                      className={({ active }) =>
                        classNames(
                          active ? 'bg-gray-50' : '',
                          'block px-3 py-1 text-sm leading-6 text-gray-900 w-full text-left',
                        )
                      }
                      onClick={handleSignOut}
                    >
                      Ieșire
                    </Menu.Item>
                    <Menu.Item
                      as='div'
                      className='text-xs px-3 py-1 bg-gray-50'
                    >
                      {import.meta.env.VITE_VERSION ?? 'edge'}+
                      {import.meta.env.VITE_REVISION ?? 'develop'}
                    </Menu.Item>
                  </Menu.Items>
                </Transition>
              </Menu>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
