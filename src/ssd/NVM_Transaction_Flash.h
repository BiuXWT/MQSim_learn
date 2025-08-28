﻿#ifndef NVM_TRANSACTION_FLASH_H
#define NVM_TRANSACTION_FLASH_H

#include <string>
#include <list>
#include<cstdint>
#include "../sim/Sim_Defs.h"
#include "../sim/Sim_Event.h"
#include "../sim/Engine.h"
#include "../nvm_chip/flash_memory/FlashTypes.h"
#include "../nvm_chip/flash_memory/Flash_Chip.h"
#include "../nvm_chip/flash_memory/Physical_Page_Address.h"
#include "NVM_Transaction.h"
#include "User_Request.h"

namespace SSD_Components
{
	class User_Request;

	class NVM_Transaction_Flash : public NVM_Transaction
	{
	public:
		NVM_Transaction_Flash(Transaction_Source_Type source, Transaction_Type type, stream_id_type stream_id,
			unsigned int data_size_in_byte, LPA_type lpa, PPA_type ppa, User_Request* user_request, IO_Flow_Priority_Class::Priority priority_class);
		NVM_Transaction_Flash(Transaction_Source_Type source, Transaction_Type type, stream_id_type stream_id,
			unsigned int data_size_in_byte, LPA_type lpa, PPA_type ppa, const NVM::FlashMemory::Physical_Page_Address& address, User_Request* user_request, IO_Flow_Priority_Class::Priority priority_class);
		NVM::FlashMemory::Physical_Page_Address Address;
		unsigned int Data_and_metadata_size_in_byte; //请求中包含的字节数：真实页面的字节数 + 元数据的字节数

		LPA_type LPA;//logical page address
		PPA_type PPA;//physical page address

		bool SuspendRequired;//是否需要暂停
		bool Physical_address_determined;//物理地址被正确翻译并赋值
		sim_time_type Estimated_alone_waiting_time;//用于调度方法，如 FLIN，在调度中考虑公平性和 QoS
		bool FLIN_Barrier;//Especially used in queue reordering in FLIN scheduler
	private:

	};
}

#endif // !FLASH_TRANSACTION_H
